from django.shortcuts import render
from django.http import JsonResponse
from .forms import CodeErrorForm
import openai

openai.api_key = "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"


# Create your views here.
def index(request):
    if request.method == "POST":
        # Code Error
        form = CodeErrorForm(request.POST)
        if form.is_valid():
            code_context = form.cleaned_data["code"]
            print(code_context)
            error_context = form.cleaned_data["error"]
            print(error_context)
            prompt = (f"Explain the error in this code without fixing it:"
                      f"\n\n{code_context}\n\nError:\n\n{error_context}"
                      )
            model_engine = "text-davinci-003"
            explanation_completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.9
            )

            explanation = explanation_completions.choices[0].text
            print(f"explanation: {explanation}")
            fixed_code_prompt = (f"Fix this code: \n\n{code_context}\n\nError:\n\n{error_context}."
                                 f"\n Respond only with the fix code."
                                 )
            fixed_code_completions = openai.Completion.create(
                engine=model_engine,
                prompt=fixed_code_prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.9,
            )
            fixed_code = fixed_code_completions.choices[0].text
            print(f"form:{form}")
            print(f"fixed code:{fixed_code}")
            form = CodeErrorForm()
            context = {
                'form': form,
                'explanation': explanation,
                'fixed_code': fixed_code,
            }
            return render(request, 'app/index.html', context)
    else:
        form = CodeErrorForm()
    context = {'form': form}
    return render(request, 'app/index.html', context)
