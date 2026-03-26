from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import IrisPlant, Location
import csv
import io

# custom user form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# API and AI libraries 
from rest_framework import viewsets
from .serializers import IrisPlantSerializer
try:
    from sklearn.datasets import load_iris
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier
except ImportError:
    pass 

# CSV operations
def export_iris_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iris_verileri.csv"'

    writer = csv.writer(response)
    writer.writerow(['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species'])
    
    plants = IrisPlant.objects.all()
    for plant in plants:
        writer.writerow([plant.sepal_length, plant.sepal_width, plant.petal_length, plant.petal_width, plant.species])
    return response

def import_iris_csv(request):
    if request.method == "POST":
        try:
            csv_file = request.FILES.get('csv_file')
            if not csv_file or not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
                return redirect('list_view')
            
            # read and parse the file
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string) 
            
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                if len(column) > 4:
                    # save to database
                    IrisPlant.objects.create(
                        sepal_length=float(column[1]) if len(column)>5 else float(column[0]),
                        sepal_width=float(column[2]) if len(column)>5 else float(column[1]),
                        petal_length=float(column[3]) if len(column)>5 else float(column[2]),
                        petal_width=float(column[4]) if len(column)>5 else float(column[3]),
                        species=column[5] if len(column)>5 else column[4]
                    )
            messages.success(request, 'Data uploaded successfully!')
            return redirect('list_view')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('list_view')
    return render(request, 'import.html')


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def list_view(request):
    # show all plants
    plants = IrisPlant.objects.all()
    return render(request, 'list.html', {'plants': plants})

def add_view(request):
    if request.method == "POST":
        # get data from form and save
        IrisPlant.objects.create(
            sepal_length=request.POST.get('sepal_length'),
            sepal_width=request.POST.get('sepal_width'),
            petal_length=request.POST.get('petal_length'),
            petal_width=request.POST.get('petal_width'),
            species=request.POST.get('species')
        )
        return redirect('list_view')
    return render(request, 'add.html')

def delete_view(request, id):
    # find and delete the plant
    plant = get_object_or_404(IrisPlant, id=id)
    plant.delete()
    return redirect('list_view')

def update_view(request, id):
    plant = get_object_or_404(IrisPlant, id=id)

    if request.method == "POST":
        # update details
        plant.sepal_length = request.POST.get('sepal_length')
        plant.sepal_width = request.POST.get('sepal_width')
        plant.petal_length = request.POST.get('petal_length')
        plant.petal_width = request.POST.get('petal_width')
        plant.species = request.POST.get('species')
        
        plant.save()
        return redirect('list_view')

    return render(request, 'update.html', {'plant': plant})

def search_view(request):
    results = IrisPlant.objects.all()
    query_species = request.GET.get('species')
    query_min = request.GET.get('min_sepal_len')
    query_max = request.GET.get('max_sepal_len')

    # filter results
    if query_species and query_species != "":
        results = results.filter(species__icontains=query_species)
    if query_min:
        results = results.filter(sepal_length__gte=query_min)
    if query_max:
        results = results.filter(sepal_length__lte=query_max)

    return render(request, 'search.html', {'results': results})


class IrisPlantViewSet(viewsets.ModelViewSet):
    queryset = IrisPlant.objects.all()
    serializer_class = IrisPlantSerializer

def predict_view(request):
    predictionResult = None
    if request.method == 'POST':
        # get inputs
        sl = request.POST.get('sl')
        sw = request.POST.get('sw')
        pl = request.POST.get('pl')
        pw = request.POST.get('pw')
        alg = request.POST.get('model_type')

        if sl and sw and pl and pw:
            try:
                # load dataset and train model
                iris = load_iris()
                x, y = iris.data, iris.target
                
                if alg == 'knn':
                    model = KNeighborsClassifier(n_neighbors=3)
                elif alg == 'svm':
                    model = SVC()
                else:
                    model = DecisionTreeClassifier()
                
                model.fit(x, y)
                pred_index = model.predict([[float(sl), float(sw), float(pl), float(pw)]])[0]
                predictionResult = iris.target_names[pred_index]
            except:
                predictionResult = "Error"

    return render(request, 'predict.html', {'result': predictionResult})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_view')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')