from django import forms

class VideoLinkForm(forms.Form):
    video_link = forms.URLField(label='Video Link', widget=forms.TextInput(attrs={'class': 'inputfield'}))