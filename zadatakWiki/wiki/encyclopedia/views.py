import markdown

from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def open(request, title):
    for entry in util.list_entries():
        if title == entry:
            return render(request, "encyclopedia/content.html", {
                "content": markdown.markdown(util.get_entry(title)),
                "title": title
            })

    return render(request, "encyclopedia/error.html", {
        "title": title
    })


def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            page_title = form.cleaned_data["title"]
            page_content = form.cleaned_data["content"]

            for entry in util.list_entries():
                if page_title == entry:
                    return render(request, "encyclopedia/error1.html", {
                        "title": page_title
                    })

            util.save_entry(page_title, "#" + page_title + "\n\n" + page_content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm()
    })
