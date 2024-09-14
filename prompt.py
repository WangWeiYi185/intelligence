
def trasnalte_prompt(texts, local): 
    print(f"Translation request: {"".join(f"{unit} \n" for unit in texts)}, local code: {local}")
    return {
        "model": "llama3.1",
        "prompt": f'''I want you to act as an translator, spelling corrector and improver. I will speak to you in any language and you will translate it, by iSO local code. I want you to only reply the Translation results, do not write explanations and suggestions。 Translate the following text 
        "{"".join(f"{unit} \n" for unit in texts)}", local code is "{local}"''',
    }