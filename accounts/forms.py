from django.contrib.auth.forms import UserCreationForm

from .models import User

TEXT_INPUT_CLASSES = (
    "w-full rounded-xl border border-slate-300 bg-white/70 px-4 py-3 text-sm "
    "text-slate-900 placeholder:text-slate-400 focus:border-rose-500 "
    "focus:outline-none focus:ring-2 focus:ring-rose-200"
)


class RailooUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "phone_number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", TEXT_INPUT_CLASSES)
            if field.label:
                field.widget.attrs.setdefault("placeholder", str(field.label))
