'''
Created on Aug 3, 2017

@author: guangnanliang
'''
from flask import Flask, request, render_template
#from StdSuites.AppleScript_Suite import result
import json 
app = Flask(__name__)

@app.route("/")
def classification():
    return render_template("Prediction.html")

@app.route("/Prediction_Respond", methods=["POST"])
def decisionforest1():
    fico = request.form["fico"]
    flag_fthb = request.form["flag_fthb"]
    cd_msa = request.form["cd_msa"]
    mi_pct = request.form["mi_pct"]
    cnt_units = request.form["cnt_units"]

    occpy_sts = request.form["occpy_sts"]
    cltv = request.form["cltv"]
    dti = request.form["dti"]
    orig_upb = request.form["orig_upb"]
    ltv = request.form["ltv"]

    int_rt = request.form["int_rt"]
    Channel = request.form["Channel"]
    ppmt_pnlty = request.form["ppmt_pnlty"]
    prop_type = request.form["prop_type"]
    loan_purpose = request.form["loan_purpose"]

    orig_loan_term = request.form["orig_loan_term"]
    cnt_borr = request.form["cnt_borr"]
    api_key = request.form["modcost"]
    url = request.form["url"]
    model = request.form["model"]
    
    data =  {
                {
                    "Inputs": {
                        "input1": {
                            "ColumnNames": [
                                "fico",
                                "flag_fthb",
                                "cd_msa",
                                "mi_pct",
                                "cnt_units",
                                "occpy_sts",
                                "cltv",
                                "dti",
                                "orig_upb",
                                "ltv",
                                "int_rt",
                                "channel",
                                "ppmt_pnlty",
                                "prop_type",
                                "loan_purpose",
                                "orig_loan_term",
                                "cnt_borr"
                            ],
                            "Values": [
                                [
                                  fico,
                                  flag_fthb,
                                  cd_msa,
                                  mi_pct,
                                  cnt_units,

                                  occpy_sts,
                                  cltv,
                                  dti,
                                  orig_upb,
                                  ltv,

                                  int_rt,
                                  Channel,
                                  ppmt_pnlty,
                                  prop_type,
                                  loan_purpose,

                                  orig_loan_term,
                                  cnt_borr     
                                ], 
                            ]
                        }, 
                    },
              "GlobalParameters": {}
            }
    }

    body = str.encode(json.dumps(data))
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers) 
    
    response = urllib.request.urlopen(req)
    result = response.read()
    return render_template('Classification_Respond.html', model=model, Scored_Label=result["Results"]["output1"]["value"]["Values"][25])

if __name__ == '__main__':
   app.run()