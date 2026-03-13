# Prompting Small LLMs (Phi‑3.5‑Mini and Similar) for Structured Extraction and Line‑Number Mapping

## Executive summary

Multiple engineering teams have successfully used small models (around 3–4B parameters) such as Phi‑3.5‑mini‑instruct and NuExtract‑1.5 (a Phi‑3.5‑mini fine‑tune) for document→JSON extraction, often in combination with OCR.  Common patterns are: (1) very explicit JSON instructions, (2) schema or grammar constraints, and (3) line‑number encoding in the input plus a schema that asks only for indices, not text.  The examples below show concrete prompts and code patterns you can adapt directly to your CNIE pipeline.[1][2][3][4][5][6]


## Phi‑3.5‑mini‑instruct: official text‑chunking prompt (JSON output)

A Microsoft TechCommunity article demonstrates using **Phi‑3.5‑mini‑instruct** to split arbitrary text into JSON chunks, with a prompt that small models follow reliably.[2]

> You are an expert in content chunking. Please help me chunk user's input text according to the following requirements  
> 1. Truncate the text content into chunks of no more than 300 tokens.  
> 2. Each chunk part should maintain contextual coherence. The truncated content should be retained in its entirety without any additions or modifications.  
> 3. Each chunked part is output JSON format { "chunking": "..." }  
> 4. The final output is a JSON array [{ "chunking" : "..." },{ "chunking" :"..."},{ "chunking" : "..."} ....]

Key takeaways for your use case:

- The task is framed very narrowly (chunking only, no extra commentary).[2]
- JSON structure is spelled out twice: once as single object, once as array of objects.[2]
- It explicitly forbids modifications of the source text ("without any additions or modifications"), which you can adapt to "copy tokens exactly from the OCR lines".

For CNIE extraction, you can mirror this style:

- Replace "chunking" with your field names.
- State that every value must come from the provided, numbered OCR lines and must never be invented.


## LLMAIx: local LLM information extraction with explicit JSON prompt + grammar

The **LLMAIx** project (KatherLab) is a concrete example of using local LLMs for information extraction and anonymization, including when the input went through OCR.  Their tutorial shows exactly how they prompt the model to return a JSON object for medical reports.[5]

Example prompt from the tutorial:

> From the following medical report, extract the following information and return it in JSON format:  
> &nbsp;&nbsp;&nbsp;&nbsp;shortness of breath: true / false  
> &nbsp;&nbsp;&nbsp;&nbsp;chest pain: true / false  
> &nbsp;&nbsp;&nbsp;&nbsp;leg pain or swelling: true / false  
> &nbsp;&nbsp;&nbsp;&nbsp;heart palpitations: true / false  
> &nbsp;&nbsp;&nbsp;&nbsp;cough: true / false  
> &nbsp;&nbsp;&nbsp;&nbsp;dizziness: true / false  
> &nbsp;&nbsp;&nbsp;&nbsp;location: main / segmental / unknown  
> &nbsp;&nbsp;&nbsp;&nbsp;side: left / right / bilateral  
>  
> This is the medical report:  
> {report}:

They combine this with a **GBNF grammar** that hard‑restricts keys and types so the model can only emit valid JSON, for example:

```bnf
root ::= allrecords

allrecords ::= (
  "{" ws "\"shortness of breath\":" ws boolean ","
  ws "\"chest pain\":" ws boolean ","
  ...
  ws "\"side\":" ws "\"" ( "left" | "right" | "bilateral" ) "\"" ","  
  ws "}"
  ws
)

boolean ::= "\"" ("true" | "false") "\"" ws
```



Relevance for your 3.8B GGUF setup:

- This is exactly the **"instruct + JSON"** style you are already using, proven to work with local models (LLama‑family and others via llama.cpp).[5]
- The **grammar/JSON‑schema layer** is used to catch and correct malformed outputs without relying on the model to always format correctly.[5]
- You can adapt the same pattern to CNIE by listing fields such as `last_name_fr`, `first_name_ar`, `cnie_number`, and optional fields with allowed enumerations.


## Instructor example: segmenting by line indices instead of regenerating text

The **Instructor** documentation has a worked example of document segmentation where the model never regenerates section text; instead it returns **start and end line indices** into a numbered document.[3]

They define a Pydantic model where each section has line indices:

```python
class Section(BaseModel):
    title: str = Field(description="main topic of this section of the document")
    start_index: int = Field(description="line number where the section begins")
    end_index: int = Field(description="line number where the section ends")

class StructuredDocument(BaseModel):
    """obtains meaningful sections, each centered around a single concept/topic"""
    sections: List[Section]
```

and preprocess the document so each line is explicitly tagged:

```python
def doc_with_lines(document):
    document_lines = document.split("\n")
    document_with_line_numbers = ""
    for i, line in enumerate(document_lines):
        document_with_line_numbers += f"[{i}] {line}\n"
    return document_with_line_numbers, line2text
```



The system prompt then tells the model:

> You are a world class educator working on organizing your lecture notes.  
> Read the document below and extract a StructuredDocument object from it where each section of the document is centered around a single concept/topic that can be taught in one lesson.  
> Each line of the document is marked with its line number in square brackets (e.g.,,, etc). Use the line numbers to indicate section start and end.

[3]

This matches your idea of **line‑ID‑only outputs**, and shows that small/medium models can do stable index assignment if:

- Line numbers are visually obvious (`[0]`, `[1]`, …) and part of the text.
- The schema exposes **only indices**, not free‑form text.


## LLMWhisperer: line‑number provenance for extraction

The **LLMWhisperer Highlighting** docs describe a practical pattern for line‑aware extraction in production.

Key steps in their design:[4]

- The OCR or preprocessor returns each line with a **line number**, and they use **hexadecimal line IDs** to make them visually distinct from other numbers in the content.[4]
- The extraction prompt instructs the LLM to **include the line numbers from which each field was extracted**.[4]
- Coordinates for each line are stored separately, so the UI can highlight exact regions when a reviewer inspects the extracted data.[4]

This confirms the approach you are using: the LLM never has to copy text perfectly; it only has to map schema fields → line IDs, and the application resolves those IDs back to OCR text.


## Deepschool.ai: comparing NuExtract, 0.5B Qwen, and Phi‑3.5‑mini for structured outputs

A deepschool.ai blog post explicitly compares **NuExtract‑tiny‑v1.5**, **Qwen‑2.5‑0.5B**, and **Phi‑3.5‑mini‑instruct** for structured output, using prompts that are close to what you need.[1]

### Template‑driven extraction

They first show a chat‑style template prompt for full JSON extraction:

```text
<|input|>
### Template:
{template}
### Text:
{text}

<|output|>
```

The `template` variable is a JSON skeleton (e.g. `"Model": {"Name": "", ...}`) and the model is simply asked to fill it from the text.  This works best with NuExtract, but they also test Phi‑3.5‑mini.[1]

### Key‑by‑key extraction with Phi‑3.5‑mini

When they switch to extracting one key at a time, they use a more detailed system prompt:[1]

```text
You are a helpful assistant that can extract values given a requested key and data type.
If you don't know, output "unknown". Be concise and precise.
Don't repeat the key in the answer!
```

Then for each key they build:

```text
### Text:
{text}
### Required Key:
{key}
```

and decode only the assistant’s final short answer.[1]

Important behaviors you can borrow for CNIE:

- **One‑field‑at‑a‑time extraction** often reduces confusion vs asking for 10 fields in one shot, especially on small models.[1]
- The instruction *"If you don't know, output \"unknown\""* is followed reasonably well even by Phi‑3.5‑mini; you can adapt that to `null` or `[]` for missing CNIE fields.[1]
- The model is explicitly told **not** to repeat the key name, which avoids redundant output and makes parsing trivial.[1]


## NuExtract 1.5: Phi‑3.5‑mini‑based multilingual extractor

NuMind’s **NuExtract 1.5** is a dedicated information‑extraction model fine‑tuned from **Phi‑3.5‑mini (3.8B)** specifically for “document → JSON” tasks.[6]

Key facts that matter for your bilingual Arabic/French ID cards:

- NuExtract 1.5 is trained to do exactly one thing: **extract JSON structures from documents** and is reported to outperform GPT‑4o on an English zero‑shot benchmark while being 500× smaller.[6]
- It is explicitly **multilingual**, based on Phi‑3.5‑mini’s support for Arabic, French, and many other languages.[6]
- Training data is **50% English and 50% other languages**, with templates sometimes in English and sometimes in the document language.[6]
- The dataset and training are **purely extractive**: the model is trained to *copy‑paste parts of the document and not generate anything new*, and to return empty results when information is missing.[6]

Although NuExtract wraps this into its own API and templates, the design strongly supports the prompting strategies you want for raw Phi‑3.5‑mini:

- Emphasize *copying substrings from the OCR lines*, never paraphrasing.
- Allow and normalize empty values instead of encouraging the model to guess.
- For multilingual documents, it is valid to keep your **system prompt in French** while still handling Arabic text, or to add a short Arabic meta‑instruction if you see confusion.


## Summary of patterns that work with small LLMs

From these real examples, several stable patterns emerge for sub‑4B models doing document/ID extraction:

| Pattern | Where it appears | Why it helps small models |
|--------|------------------|---------------------------|
| Number each input line and treat line IDs as first‑class data | Instructor doc segmentation, LLMWhisperer highlighting[3][4] | Avoids regeneration errors and lets the model operate in index space. |
| Constrain output to strict JSON via grammar or schema | LLMAIx grammar, JSON Schema[5] | Removes many formatting errors and enforces keys/types. |
| Make the task extremely narrow (chunking only, or one key at a time) | Microsoft chunking prompt, Deepschool key‑by‑key extraction[2][1] | Reduces cognitive load and cross‑field interference. |
| Explicitly allow “unknown” / empty outputs | Deepschool Phi‑3.5 prompt, NuExtract’s extractive training[1][6] | Discourages hallucinations when OCR is noisy. |
| Keep prompts short but very explicit about structure | All examples above | Smaller context and clearer constraints improve reliability. |


## How to adapt these to your CNIE OCR pipeline

Based on the above, a robust prompt template for **line‑ID mapping with Phi‑3.5‑mini‑instruct** could look like this (in French to match most CNIE labels, but still handling Arabic lines):

```text
Vous êtes un système d’extraction de données qui ne renvoie que du JSON.
Votre tâche est de lire une liste de lignes OCR numérotées et d’indiquer, pour chaque champ, 
LES NUMÉROS DE LIGNES d’où proviennent les valeurs.

Règles importantes :
- Utilisez exactement les numéros de ligne entre crochets, par exemple [0], [1], [2]…
- Ne copiez JAMAIS le texte des lignes, ne traduisez pas et ne reformulez pas.
- Si une information est absente ou illisible, mettez [] pour ce champ.
- Ne renvoyez AUCUN autre texte que le JSON demandé.

Voici les champs à extraire (les valeurs réelles seront reconstruites ensuite par un autre programme) :
- last_name_fr : nom de famille en français
- first_name_fr : prénom en français
- last_name_ar : nom de famille en arabe
- first_name_ar : prénom en arabe
- cnie_number : numéro de carte nationale
- birth_date : date de naissance
- birth_place_fr : lieu de naissance en français
- birth_place_ar : lieu de naissance en arabe

Format de sortie JSON OBLIGATOIRE :
{
  "last_name_fr": [listes de numéros de lignes],
  "first_name_fr": [...],
  "last_name_ar": [...],
  "first_name_ar": [...],
  "cnie_number": [...],
  "birth_date": [...],
  "birth_place_fr": [...],
  "birth_place_ar": [...]
}

Maintenant, voici les lignes OCR numérotées :
[0] ...
[1] ...
[2] ...
...
```

This combines:

- The **line‑number conventions** from Instructor and LLMWhisperer.[3][4]
- The **strict JSON output** and explicit field descriptions from LLMAIx.[5]
- The **non‑hallucination rules** and willingness to leave fields empty from the NuExtract and Deepschool patterns.[6][1]

For even more stability with a 3.8B model, you can:

- Run **one or two fields per call** (Deepschool technique) in difficult cases like Arabic names vs French surnames.[1]
- Add a simple grammar or JSON‑schema layer (LLMAIx approach) to guarantee syntactic correctness, then automatically retry when the model fails validation.[5]
- Keep the French system prompt but include a short Arabic sentence such as “انسخ النص كما هو من السطور ولا تخترع أي معلومات” (“copy the text exactly from the lines and do not invent any information”) if you notice confusion on Arabic‑only cards.[6]

These patterns are all used in real systems with small models, and they transfer well to your Phi‑3.5‑mini‑instruct + llama‑cpp‑python CNIE pipeline.