from django import forms

# options for the AI model
ALGORITHM_CHOICES=[
    ('knn', 'K-Nearest Neighbors (KNN)'),
    ('svm', 'Support Vector Machine (SVM)'),
    ('dt', 'Decision Tree')
]

class PredictionForm(forms.Form):
    # inputs for the flower measurements
    sl = forms.FloatField(label='Sepal Length', min_value=0, required=True)
    sw = forms.FloatField(label='Sepal Width', min_value=0, required=True)
    pl = forms.FloatField(label='Petal Length', min_value=0, required=True)
    pw = forms.FloatField(label='Petal Width', min_value=0, required=True)
    
    # choose the algorithm
    model_type = forms.ChoiceField(choices=ALGORITHM_CHOICES, label='Algorithm')