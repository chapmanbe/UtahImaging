import os
import glob
import subprocess
import sqlite3 as sq
import time
import re
# In[3]:

#sdir = "/Volumes/phenotyping2/LungSegmentation"
#idir = "/Volumes/phenotyping2/PittVolumes"
sdir = "/media/brian/CCTS/LungSegmentation2"
idir = "/media/brian/CCTS/PittVolumes"





def getScores(scores):
    try:
        prompt = "; ".join(["%d: %s"%(i,scores[i]) for i in range(len(scores))])
        return scores[int(raw_input(prompt))]
    except IndexError:
        print "selection our of range"
        return getScores(scores)
    except (NameError, ValueError):
        print "must enter a number"
        return getScores(scores)


# In[27]:

def createTables(cursor):
    q1 = """CREATE TABLE IF NOT EXISTS sensitivity_schema(score int, value text)"""
    q2 = """CREATE TABLE IF NOT EXISTS specificity_schema(score int, value text)"""
    q3 = """CREATE TABLE IF NOT EXISTS """
    q3 += """review(case_num text, sensitivity int,specificity int,sens_schema int, spec_schema int, comment text,"""
    q3 += """FOREIGN KEY(sens_schema) REFERENCES sensitivity_schema(rowid), FOREIGN KEY(spec_schema) REFERENCES specificity_schema(rowid))"""
    cursor.execute(q1)
    cursor.execute(q2)
    cursor.execute(q3)
    


# In[28]:

def saveSchema(cursor,table,schema):
    query = """INSERT INTO %s(value) VALUES (?)"""%table
    cursor.execute(query,schema)
    return cursor.lastrowid
    


# In[44]:
def main():
    files = glob.glob(os.path.join(idir,"__RV*.nii.gz"))

    conn = sq.connect("./lung_segmentation_review2.sqlite")
    cursor = conn.cursor()
    createTables(cursor)
    conn.commit()

    senslabels = ("missing all of lung","missing substantial portions of lung","captured most of lung","captured all of lung")
    sens = zip(range(len(senslabels)),senslabels)
    sens_schema = "; ".join(["%d: %s"%(s[0],s[1],) for s in sens])

    which_sens = saveSchema(cursor,"sensitivity_schema",(sens_schema,))

    speclabels = ("entirely all non-lung","captured large portion of non-lung region","captured small amoung of non-lung","did not capture non-lung")
    spec = zip(range(len(speclabels)),speclabels)
    spec_schema = "; ".join(["%d: %s"%(s[0],s[1],) for s in spec])
    which_spec = saveSchema(cursor,"specificity_schema",(spec_schema,))

    for f in files:
        cursor.execute("""SELECT case_num FROM review""")
        reviewed_cases = [r[0] for r in cursor.fetchall()]
        fseg = os.path.join(sdir,os.path.basename(f))
        #r1 = re.compile(r"""%s"""%f.split("_Exam")[0])
        #if os.path.exists(fseg) and not r1.findall(" ".join([r[0] for r in reviewed_cases])):
        if os.path.exists(fseg) and not f in reviewed_cases:
            print f
            subprocess.call("""itksnap -g %s -s %s"""%(f,fseg),shell=True)
            #time.sleep(15)
            sensitivity = getScores(senslabels)
            specificity = getScores(speclabels)
            comments = raw_input("Comments\n")
            cursor.execute("""INSERT INTO review(case_num, sensitivity, specificity, sens_schema, spec_schema, comment) VALUES (?,?,?,?,?,?)""",
                        (f,sensitivity,specificity,which_sens,which_spec,comments,))
            conn.commit()
            if os.path.exists("snapshot0001.png"):
                os.rename("snapshot0001.png",os.path.basename(f)+".png")
                    

if __name__ == '__main__':
    main()
