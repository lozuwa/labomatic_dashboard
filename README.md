A minimal dashboard example. 
TODO:
1. Media files cannot be found or serve
   Desc: settings.py has the path to media and the urlpatterns in debug mode are appended. WTF why is it not working?
2. Find how to run a GPU routine without having to use Popen 
   Desc: In order to run the Image Detection model I have to use a Popen to run another script. Eventually celeris 
         has to be included in the project to manage multitasking. 
3. Create a client connection script in order to connect to Firebase.
   Desc: So far, we have been using a local file based logic which is not scalable. Firebases' logic for the android
         app is developed. But the web part is missing. 
4. Implemet a table and the logic to change types of diagnostic in order to support my multiple models.
   Desc: Currently I have to hardcode which model I want to use. Create the logic to change the model.
