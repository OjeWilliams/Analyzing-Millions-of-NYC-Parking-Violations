mappings = {
  "settings": {
    "number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "plate": { "type": "text" },
      "state": { "type": "text" },
      "license_type": { "type": "text" },
      
      
      "issue_date": { "type": "date","format": "yyyy-MM-dd"},
      "violation_time": { "type": "text" },
      "violation": { "type": "text" },
      "judgment_entry_date": { "type": "text" },
      
      "precinct": { "type": "text" },
      "county": { "type": "text" },
      "issuing_agency": { "type": "text" },
      "violation_status": { "type": "text" },
     # "summons_image": { "type": "string" },
      
      
      "summons_number": { "type": "int" },
      "penalty_amount": { "type": "float" },
      "fine_amount": { "type": "float" },
      "interest_amount": { "type": "float" },
      "reduction_amount": { "type": "float" },
      "payment_amount": { "type": "float" },
      "amount_due": { "type": "float" },
    }
  }
}



# defined a function that checks for keys inside a list of dictionaries and makes a default key if it is missing

def make_key(w):
    field = ['fine_amount','penalty_amount',
    'interest_amount','reduction_amount','amount_due',
    'payment_amount']

    for dic in w:
        for i in field:
            if(i in dic.keys()):
                pass
                #print("The key/field is already present")
            else:
                dic[i] = 0 #  set the default to 0.0 to make float transform work
    return w
    

# define a function that checks for key if not present assign it a default value of None
def key_check(k):
    field = ['fine_amount','penalty_amount',
    'interest_amount','reduction_amount','amount_due',
    'payment_amount']

    for a in field:
        if a in k[0]:
            print("The field exist already")
            # do nothing
            pass
        else:
            k[0][a] = 0.0 # set this to zero so that float works in mappings
    return k    