# Verbs Conjugation
In this project, you can enter a verb in romanian, and it will add it's conjugation in Prezent time to a csv file. You can also search for a specific verb (to see if it is in that file), or display all of the verbs (which will display all of the verbs from that csv file in your terminal).

# How to use

Firstly let's see how you can add a verb to a file. 
To do this, you will have to create a csv file. For demonstration purposes you will create a file `test.csv` in the same directory. (Note: you can call this file anything).

After this you can run 
```
python3 main.py test.csv
```

Where you will be presented with an input field. There you can enter any verb/verbs in romanian. When you are done entering the verbs you should press `control + D` to save the verbs to the file. You will not be able to enter any verb that is not an actual verb, or a verb that is already in the csv file.


Now after you have added a verb or two, you can acess two modes. 
```
python3 main.py test.csv -d
```
Will display all of the verbs you have in that file in your terminal in a table form.

```
python3 main.py test.csv -s
```
Will let you search for a verb in the csv file (make sure you enter it in the infinitive form)
