## Format
This parser expects a JSON file with the following structure:
```json
{
"classes" : {
    "MyClassName" : {
        ...
      }
  }
}
```

Within the classes object each property will represent a class, the name of the class will be its key and its definition,
an object.

### Class Definition
A class definition is an object whose properties can contain any value which JSON accepts, that is:
- Numbers
- Strings
- Lists
- Objects

So for example, the following would define a valid class within this format:
```json
{
"classes": {
    "MyClassName": {
        "myIntProp": 13,
        "myFloatProp": 13.0,
        "myStrProp": "DummyValue",
        "myListProp": [1, 4, "Word", ["Inner", "List", "Values"]],
        "myObjProp": {
            "innerProp" : 3
         }
      }
  }
}
```
Classes can be named anything you want.

### Class Inheritance
It is possible to inherit the properties of another class by using a specially reserver keywork `Inherits` as a property
for a class. This property MUST be a list of strings where each string is the name of another class within the `classes` object.

The order of definition does not matter so long as it is properly named.

Example:
```json
"classes": {
    "MyClassName": {
        "myIntProp": 13,
        "myFloatProp": 13.0,
        "myStrProp": "DummyValue",
        "myListProp": [1, 4, "Word", ["Inner", "List", "Values"]],
        "myObjProp": {
            "innerProp" : 3
         }
      },
      "SecondClassName" : {
        "Inherits": ["MyClassName"],
        "childProp": "This is a new value",
        "myStrProp": "This is overwritten by child"
      }
  }
  ```
  
  As per standard inheritance rules, children will inherit all properties from their parents and if a property is redefined
  within the child then that value is the one that will be written.
  
  The JSON above once parsed produces the following result:
  
  ```json
  "MyClassName": {
    "myFloatProp": 13.0,
    "myListProp": [1, 4, "Word", ["Inner", "List","Values"]],
    "myIntProp": 13,
    "myObjProp": {
      "innerProp": 3
    },
    "myStrProp": "DummyValue"
  },
  "SecondClassName": {
    "myFloatProp": 13.0,
    "myIntProp": 13,
    "myObjProp": {
      "innerProp": 3
    },
    "myStrProp": "This is overwritten by child",
    "myListProp": [1, 4, "Word", ["Inner", "List","Values"]],
    "childProp": "This is a new value"
  }
  ```
It is important to note that the order of the properties is not important, but rest assured that inheritance is always
solved first.

### Private properties
It is also possible to define properties that are private to that class, that is, will not be inherited by any class
that derives from them. this is done by prefixing the name of the property that will be private with the string `$_`.

Example:

```json
{
"classes" : {
    "MyClassName" : {
        "$_MyPrivateProp": "This will not be inherited",
        "PublicProp": "This will be inherited"
     },
     "MyOtherClass": {
      "Inherits": ["MyClassName"]
     }
  }
}
```
The above JSON produces as a result:

```json
{
  "MyClassName" : {
      "MyPrivateProp": "This will not be inherited",
      "PublicProp": "This will be inherited"
   },
   "MyOtherClass": {
     "PublicProp": "This will be inherited"
   }
}
```

Notice that the private prefix is dropped on the parsed result.

### Class Reference
Class definitions also allow to reference another class in order to create an "instance" of that class,
this is useful for composing classes in lists or other properties.

In order to reference another class simply write a string value which is the name of another class prefixed with the string
`ref_`:

E.g: `ref_MyClassName`

Usage example:

```json
{
"classes" : {
    "SwordClass" : {
        "name": "Sword",
        "weight": 50,
        "sharpness": 10
     },
     "ShieldClass": {
      "name": "Shield",
      "defense": 50
     },
     "WandClass": {
      "name": "Wand",
      "magic": 30
     },
     "BackpackClass": {
       "name": "Backpack",
       "contents": ["ref_SwordClass", "ref_ShieldClass", "ref_WandClass"]
     }
  }
}
```

The code above produces the following result:

```json
{
  "ShieldClass": {
    "name": "Shield",
    "defense": 50
  },
  "WandClass": {
    "name": "Wand",
    "magic": 30
  },
  "SwordClass": {
    "name": "Sword",
    "weight": 50,
    "sharpness": 10
  },
  "BackpackClass": {
    "name": "Backpack",
    "contents": [
      {
        "name": "Sword",
        "weight": 50,
        "sharpness": 10
      },
      {
        "name": "Shield",
        "defense": 50
      },
      {
        "name": "Wand",
        "magic": 30
      }
    ]
  }
}
```

## Script Usage
Simply run the script `main.py` with your formatted JSON using Python version 3.5 or above.

E.g: `python3 main.py my_json_file.json`

This will generate an `output.json` file with the parsed result.
