from flask import Flask, request, render_template, redirect
import connect
# import threading
import csv
import re
import category_to_url
import benutzer
import projekt
#import konto
import kommentar
import schreibt
import spenden
import newprojectStore
#import benutzerStore
import fetchprojects
import fetchuser
import fetchinfo
import fetchnewprojectfund
import fetchnewcomment
import fetchinfotoedit
import fetchdelete
import fetchsearch


app = Flask(__name__, template_folder='template')

#############################  SETING FOR SERVER PROPERTIES  #################################
def csv_reader(path):
    with open(path, "r") as csvfile:
        tmp = {}
        reader = csv.reader(csvfile, delimiter='=')
        for line in reader:
            tmp[line[0]] = line[1]
    return tmp

config = csv_reader("properties.settings")

############################     BENUTZER DATA      ###########################################
userList = []    #list of object benutzer
userList.append(benutzer.Benutzer('dummy@dummy.com', 'DummyUser', 'I am a dummy user!'))
userList.append(benutzer.Benutzer('alan@turing.com', 'Alan Turing', 'I like computers'))
userList.append(benutzer.Benutzer('donald@eKnuth.com', 'DonaldEKnuth', 'I like techn innovations'))
userList.append(benutzer.Benutzer('tim@bernersLee.com', 'Tim Berners Lee', 'I love the WWW'))
userList.append(benutzer.Benutzer('alex@john.com', 'alexjohn', 'I love reading'))
userList.append(benutzer.Benutzer('fun@gmail.com', 'Fin', 'I love thinking'))
userList.append(benutzer.Benutzer('jeni@gmail.com', 'Jenifer', 'I love philosophy'))
userList.append(benutzer.Benutzer('camy@gmail.com', 'Camy', 'I love tech'))

#########################  LOGIN:   CURRENT USER  ###############################################
current_user = userList[0]
#################################################################################################
#################################################################################################
#########################     VIEW_MAIN     #####################################################
@app.route('/view_main', methods=['GET'])
def viewmainGet():
    try:
        dbExists = connect.DBUtil().checkDatabaseExistsExternal()
        if dbExists:
            db2exists = 'vorhanden! Supi!'
        else:
            db2exists = 'nicht vorhanden :-('
    except Exception as e:
        print(e)

    dataopen=[]
    dataclose=[]
    try:
        proj =  fetchprojects.Fetchprojects()
        openprojects = proj.fetchopenprojects()
        closeprojects = proj.fetchcloseprojects()
        for row in openprojects:
            caturl = category_to_url.cat_to_url(row[1])
            dataopen.append((row[0], caturl, row[2], row[3], row[4], row[5]))
        for row in closeprojects:
            caturl = category_to_url.cat_to_url(row[1])
            dataclose.append((row[0], caturl, row[2], row[3], row[4], row[5]))
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('view_main.html', db2exists=db2exists, dataopen=dataopen, dataclose=dataclose, current_user=current_user)

###################################################################################################
###################################################################################################
#########################    VIEW_PROJECT    ######################################################
@app.route('/view_project', methods=['GET'])
def viewprojectGet():
    kennung = request.args.get('kennung')
    kennung = int(kennung)
    info=[]
    try:
        proj = fetchinfo.Fetchinfo()
        info_project = proj.info_projekt(kennung)
        info_sumspenden = proj.info_sumspenden(kennung)
        if info_sumspenden==[(None,)]:
            info_sumspenden=0
        else:
            info_sumspenden=float(info_sumspenden[0][0])
        info_vorgaenger= proj.info_vorgaenger(kennung)
        spendList = proj.info_spendenlist(kennung)
        kommentList =  proj.info_from_kommentar(kennung)
        for row in info_project:
            caturl = category_to_url.cat_to_url(row[0])
            info.append((kennung, caturl, row[1], row[2], row[3], row[4], row[5], row[6]))
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('view_project.html', info=info,  info_sumspenden=info_sumspenden,info_vorgaenger=info_vorgaenger, spendList=spendList, kommentList= kommentList)

#############################################################################################################
#############################################################################################################
####################   NEW_PROJECT  #########################################################################
@app.route('/new_project', methods=['GET'])
def newprojectGet():
    try:
        proj = fetchuser.Fetchuser()
        vorgaenger=proj.fetchvorgaenger(current_user.email)
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('new_project.html', vorgaenger=vorgaenger)
#**********************************************************************************************************
@app.route('/new_project', methods=['POST'])
def newprojectPost():
    ititle = request.form.get('title')
    ibeschreibung = request.form.get('beschreibung')
    ilimit = request.form.get('limit')
    ilimit = float(ilimit)
    iersteller = current_user.email
    ivorgaenger = request.form.get('vorganger')
    ivorgaenger= int(ivorgaenger)
    icategory = request.form.get('category')
    icategory = int(icategory)
    try:
        proj = newprojectStore.NewprojectStore()
        ikennung= int(proj.maxkennung()[0][0]) +1
        projectToAdd = projekt.Projekt(ikennung, ititle, ibeschreibung, ilimit, iersteller, ivorgaenger, icategory)
        if projectToAdd.getvorgaenger():
            proj.addProject1(projectToAdd)
        else:
            proj.addProject2(projectToAdd)
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return redirect('/view_main')

###########################################################################################################
###########################################################################################################
######################## VIEW_PROFILE  ####################################################################
@app.route('/view_profile', methods=['GET'])
def viewprofileGet():
    user_email = request.args.get('user_email')
    user_name = request.args.get('user_name')
    dataerstellt=[]
    dataunterstutzt=[]
    try:
        proj = fetchuser.Fetchuser()
        project_erstellt=proj.fetch_erstellte_project(user_email)
        project_unterstutzt=proj.fetch_unterstutzt_project(user_email)
        project_unterstutztall=proj.fetch_unterstutzt_all(user_email)
        num_erstellt = len(project_erstellt)
        num_unterstutzt = len(project_unterstutztall)
        for row in project_erstellt:
            caturl=category_to_url.cat_to_url(row[1])
            dataerstellt.append((caturl, row[0], row[2], row[3],row[4]))
        for row in project_unterstutzt:
            caturl=category_to_url.cat_to_url(row[1])
            dataunterstutzt.append((caturl, row[0], row[2], row[3],row[4], row[5]))
            proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('view_profile.html',user_email=user_email, user_name=user_name, num_erstellt=num_erstellt, num_unterstutzt=num_unterstutzt, dataerstellt=dataerstellt, dataunterstutzt=dataunterstutzt)


############################################################################################################
############################################################################################################
######################## NEW_PROJECT_FUND  #################################################################
@app.route('/new_project_fund', methods=['GET'])
def newprojectfundGet():
    kennung = request.args.get('kennung')
    kennung = int(kennung)
    try:
        proj = fetchnewprojectfund.Fetchnewprojectfund()
        spenderList = proj.spenderList(kennung)
        name_status=proj.titel_status(kennung)
        balanceinfo = proj.kontoinfo(current_user.email)
        print("Your current balance: ", balanceinfo)
        if (current_user.email,) in spenderList:
            alreadyspend= True
        else:
            alreadyspend = False
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('new_project_fund.html', kennung=kennung, name_status=name_status, alreadyspend=alreadyspend, balanceinfo = balanceinfo)
#***********************************************************************************************************
@app.route('/new_project_fund', methods=['POST'])
def newprojectfundPost():
### INSERT NEW DONATION TO DATABASE
    kennung = request.form.get('kennung')
    kennung = int(kennung)
    sichtbarkeit = request.form.get('sichtbarkeit')
    amount = request.form.get('amount')
    amount = float(amount)
    try:
        proj = fetchnewprojectfund.Fetchnewprojectfund()
        spendentoAdd = spenden.Spenden(current_user.email, kennung, amount, sichtbarkeit)
        proj.addSpenden(spendentoAdd)
        proj.updatekonto(amount, current_user.email)
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()

#****************************************************************************
##PREPARE DATA TO REDIRECT TO VIEW_PROJECT                                   *
#****************************************************************************
    info=[]
    try:
        proj = fetchinfo.Fetchinfo()
        info_project = proj.info_projekt(kennung)
        info_sumspenden = proj.info_sumspenden(kennung)
        print(info_sumspenden)
        if info_sumspenden==[(None,)]:
            info_sumspenden=0
        else:
            info_sumspenden=float(info_sumspenden[0][0])
        info_vorgaenger= proj.info_vorgaenger(kennung)
        spendList = proj.info_spendenlist(kennung)
        kommentList =  proj.info_from_kommentar(kennung)
        for row in info_project:
            caturl = category_to_url.cat_to_url(row[0])
            info.append((kennung, caturl, row[1], row[2], row[3], row[4], row[5], row[6]))
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('view_project.html', info=info,  info_sumspenden=info_sumspenden,info_vorgaenger=info_vorgaenger, spendList=spendList, kommentList= kommentList)



###########################################################################################################
###########################################################################################################
############################ NEW_COMMENT PAGE #############################################################
@app.route('/new_comment', methods=['GET'])
def newcommentGet():
### INSERT NEW COMMENT TO DATABASE
    kennung = request.args.get('kennung')
    kennung = int(kennung)
    try:
        proj = fetchnewcomment.Fetchnewcomment()
        projectname=proj.titel(kennung)
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('new_comment.html', kennung=kennung, projectname=projectname)
#************************************************************************************************************
@app.route('/new_comment', methods=['POST'])
def newcommentPost():
    ibenutzer = current_user.email
    kennung = request.form.get('kennung')
    kennung = int(kennung)
    isichtbarkeit = request.form.get('sichtbarkeit')
    itext = request.form.get('kommentar')
    try:
        proj = fetchnewcomment.Fetchnewcomment()
        kommentarid = int(proj.maxid()[0][0]) + 1
        kommentartoAdd=kommentar.Kommentar(kommentarid,itext,isichtbarkeit)
        schreibttoAdd=schreibt.Schreibt(ibenutzer,kennung,kommentarid)
        proj.addKommentar(kommentartoAdd)
        proj.addSchreibt(schreibttoAdd)
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
# ****************************************************************************
##PREPARE DATA TO REDIRECT TO VIEW_PROJECT                                   *
# ****************************************************************************
    info=[]
    try:
        proj = fetchinfo.Fetchinfo()
        info_project = proj.info_projekt(kennung)
        info_sumspenden = proj.info_sumspenden(kennung)
        print(info_sumspenden)
        if info_sumspenden==[(None,)]:
            info_sumspenden=0
        else:
            info_sumspenden=float(info_sumspenden[0][0])
        print(info_sumspenden)
        info_vorgaenger= proj.info_vorgaenger(kennung)
        spendList = proj.info_spendenlist(kennung)
        kommentList =  proj.info_from_kommentar(kennung)
        for row in info_project:
            caturl = category_to_url.cat_to_url(row[0])
            info.append((kennung, caturl, row[1], row[2], row[3], row[4], row[5], row[6]))
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('view_project.html', info=info,  info_sumspenden=info_sumspenden,info_vorgaenger=info_vorgaenger, spendList=spendList, kommentList= kommentList)

#########################################################################################################
#########################################################################################################
######################## EDIT_PROJECT  ##################################################################
@app.route('/edit_project', methods=['GET'])
def editprojectGet():
    kennung = request.args.get('kennung')
    kennung = int(kennung)
    try:
        proj = fetchinfotoedit.Fetchinfotoedit()
        vorgaenger = proj.vorgaengerList(current_user.email, kennung)
        name_status = proj.titel_status(kennung)
        project_vorgaenger = proj.previous_vorgaenger(kennung)
        olddata = proj.previousinfo(kennung)
        if current_user.email == olddata[0][3]:
            notowner = False
        else:
            notowner = True
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    print('end of get method')
    return render_template('edit_project.html', name_status=name_status, kennung=kennung, vorgaenger=vorgaenger, project_vorgaenger=project_vorgaenger, olddata=olddata, notowner=notowner)
#****************************************************************************************************
@app.route('/edit_project', methods=['POST'])
def editprojectPost():
    ikennung=request.form.get('kennung')
    ikennung=int(ikennung)
    ititle = request.form.get('title')
    ibeschreibung = request.form.get('beschreibung')
    ilimit = request.form.get('limit')
    ilimit = float(ilimit)
    iersteller = current_user.email
    ivorgaenger = request.form.get('vorganger')
    ivorgaenger=int(ivorgaenger)
    icategory = request.form.get('category')
    icategory = int(icategory)
    try:
        proj = fetchinfotoedit.Fetchinfotoedit()
        projectToUpdate = projekt.Projekt(ikennung, ititle, ibeschreibung, ilimit, iersteller,ivorgaenger,icategory)
        if projectToUpdate.getvorgaenger():
            proj.updateProject1(projectToUpdate)
        else:
            proj.setnullfirst(ikennung)
            proj.updateProject2(projectToUpdate)
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()

# ****************************************************************************
##PREPARE DATA TO REDIRECT TO VIEW_PROJECT                                   *
# ****************************************************************************
    info = []
    try:
        proj = fetchinfo.Fetchinfo()
        info_project = proj.info_projekt(ikennung)
        info_sumspenden = proj.info_sumspenden(ikennung)
        if info_sumspenden == [(None,)]:
            info_sumspenden = 0
        else:
            info_sumspenden = float(info_sumspenden[0][0])
        info_vorgaenger = proj.info_vorgaenger(ikennung)
        spendList = proj.info_spendenlist(ikennung)
        kommentList = proj.info_from_kommentar(ikennung)
        for row in info_project:
            caturl = category_to_url.cat_to_url(row[0])
            info.append((ikennung, caturl, row[1], row[2], row[3], row[4], row[5], row[6]))
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('view_project.html', info=info, info_sumspenden=info_sumspenden, info_vorgaenger=info_vorgaenger,
                           spendList=spendList, kommentList=kommentList)
########################################################################################################
########################################################################################################
########################   DELETE PROJECT       ########################################################
@app.route('/delete_project', methods=['GET'])
def deleteprojectGet():
    kennung = request.args.get('kennung')
    kennung = int(kennung)
    try:
        proj = fetchdelete.Fetchdelete()
        name_creator=proj.titel_creator(kennung)
        if current_user.email == name_creator[0][1]:
            notowner = False
        else:
            notowner = True
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('delete_project.html',kennung=kennung, notowner=notowner, name_creator=name_creator)
# #**********************************************************************************
@app.route('/delete_project', methods=['POST'])
def deleteprojectPost():
    kennung = request.form.get('kennung')
    kennung = int(kennung)
    print('Project deleted:', kennung)
    try:
        proj = fetchdelete.Fetchdelete()
        spendenList = proj.spenderList(kennung)
        print(spendenList)
        childrenList=proj.childList(kennung)
        print('Children Projects: ', childrenList)
        if childrenList:
            proj.updateVorgaenger(childrenList)
        if spendenList:
            for eachspender in spendenList:
                proj.payback(eachspender[2], eachspender[0])
        proj.deletespenden(kennung)
        kommentarid=proj.kommentaridList(kennung)
        if kommentarid:
            for eachid in kommentarid:
                proj.deleteschreibt(eachid[0])
                proj.deletekommentar(eachid[0])
        proj.deleteproject(kennung)
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
# ****************************************************************************
#            PREPARE DATA TO REDIRECT TO VIEW_MAIN                           *
# ****************************************************************************
    try:
        dbExists = connect.DBUtil().checkDatabaseExistsExternal()
        if dbExists:
            db2exists = 'vorhanden! Supi!'
        else:
            db2exists = 'nicht vorhanden :-('
    except Exception as e:
        print(e)

    dataopen=[]
    dataclose=[]
    try:
        proj =  fetchprojects.Fetchprojects()
        openprojects = proj.fetchopenprojects()            #list of tuples
        closeprojects = proj.fetchcloseprojects()
        for row in openprojects:
            caturl = category_to_url.cat_to_url(row[1])
            dataopen.append((row[0], caturl, row[2], row[3], row[4], row[5]))
        for row in closeprojects:
            caturl = category_to_url.cat_to_url(row[1])
            dataclose.append((row[0], caturl, row[2], row[3], row[4], row[5]))
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('view_main.html', db2exists=db2exists, dataopen=dataopen, dataclose=dataclose, current_user=current_user)


##########################################################################################################
##########################################################################################################
########################     SEARCH       ################################################################
@app.route('/search', methods=['GET'])
def searchGet():
    results=[]
    phrase=''
    return render_template('search.html', results=results, phrase=phrase)

#***************************************************************************************
@app.route('/search', methods=['POST'])
def searchPost():
    keyword = request.form.get('searchword')
    results=[]
    try:
        proj = fetchsearch.Fetchsearch()
        projects=proj.projects(keyword)
        print(projects)
        if projects:
            for row in projects:
                print(row[0])
                info=proj.projectinfo(row[0])
                print(info)
                caturl = category_to_url.cat_to_url(info[0][1])
                results.append((caturl, info[0][2], info[0][3], info[0][4],info[0][5]))
            phrase=''
        else:
            results=[]
            phrase = 'No matched results'
        proj.completion()
    except Exception as e:
        print(e)
        return "Failed!"
    finally:
        proj.close()
    return render_template('search.html', results=results, phrase=phrase)

###########################################################################################################
###########################################################################################################
########################     RUN APP       ################################################################
if __name__ == "__main__":
    port = int("9" + re.match(r"([a-z]+)([0-9]+)", config["username"], re.I).groups()[1])
    app.run(host='0.0.0.0', port=port, debug=True)
