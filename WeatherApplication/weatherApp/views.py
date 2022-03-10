from django.shortcuts import render
import urllib.request
import json
import wikipediaapi

def index(request):
    data = {}
    data["country_code"] = "NotSearched"
    if request.method == 'POST':
        city = request.POST['city']
        city = city.replace(" ", "+")
        try:
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + 
                city + '&units=metric&appid=074e542b37c5221c9fe121e23c9ad2be').read()

            listOfData = json.loads(source)

            data = {
                "name" : str(listOfData['name']),
                "country": str(listOfData['sys']['country']),
                "coordinates": str(listOfData['coord']['lat']) + ', ' + str(listOfData['coord']['lon']),
                "temperature": str(listOfData['main']['temp']) + ' °C',
                "pressure": str(listOfData['main']['pressure']) + ' hPa',
                "humidity": str(listOfData['main']['humidity']) + '%',
                'description': str(listOfData['weather'][0]['description']),
                'icon': listOfData['weather'][0]['icon'],
            }
        except:
            data["country_code"] = "NotAvailable"

        try:
            city = city.replace("+", "-")
            photoSource = urllib.request.urlopen(f"https://api.teleport.org/api/urban_areas/slug:{city.lower()}/images").read()
            photosList = json.loads(photoSource)
            photoLink = str(photosList['photos'][0]['image']['web'])
            data['cityPhoto'] = photoLink
        except:
            pass
        
        try:
            city = city.replace("-", "_")
            wiki_wiki = wikipediaapi.Wikipedia('en')
            page_py = wiki_wiki.page(city)
            definition = page_py.summary[0:400]
            for i in range(200, 400):
                if (definition[i] == '.' 
                    and definition[i+1] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] 
                    and definition[i+2].lower() != definition[i+2]):
                    definition = definition[0:i]
                    break
            data['definition'] = definition
        except:
            pass

        
        
    return render(request, "index.html", data)