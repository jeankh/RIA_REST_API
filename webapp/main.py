from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from webapp.models import Enseignant, Etudiant, Filiere, UE, Cours, EDT, Utilisateur
from webapp.database import db
import datetime
from dateutil.parser import parse



app = Flask(__name__, template_folder="../templates")


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///edt.db"

db.init_app(app)
with app.app_context():
    db.create_all()

def reset_database():
    db.session.query(Etudiant).delete()
    db.session.query(Enseignant).delete()
    db.session.query(Filiere).delete()
    db.session.query(UE).delete()
    db.session.query(Cours).delete()
    db.session.query(EDT).delete()
    db.session.commit()


#------------Populate-----------------------------------
@app.route("/populate")
def populate_db():
    reset_database()
    prof1= Enseignant(id_utilisateur = 2 , responsabilite_ens = 'Professeur', volume_horaire = 192)
    filiere1 = Filiere(id_filiere = 1, nom_filiere = 'm1', description = 'cest cool!', niveau = 'M', 
                      nombre_annee = 1,  id_responsable =  prof1.id_utilisateur)
    etudiant1 = Etudiant(id_utilisateur = 0, diplome_etudiant = 'l3', id_filiere = filiere1.id_filiere)
    ue1 = UE(id_ue = 3, id_filiere = filiere1.id_filiere, libelle_ue = 'cest pas complique!', description = 'du tout')
    cours1 = Cours(id_cours=4, id_enseignant= prof1.id_utilisateur, id_ue= ue1.id_ue)
    edt = EDT(id_edt = 1, id_filiere = filiere1.id_filiere, id_cours = cours1.id_cours, date_debut = datetime.datetime.now(), date_fin = datetime.datetime.now(), type_cours = 'td')

                      

    db.session.add_all( [prof1, filiere1, etudiant1, ue1, cours1, edt])
    db.session.commit()
    return redirect(url_for("get_enseignants"))


#------------Enseignant-----------------------------------

@app.route('/enseignants')
def get_enseignants():
    enseignants = Enseignant.query.all()
    return jsonify([enseignant.serialize() for enseignant in enseignants])


@app.route("/enseignant/<id_utilisateur>")
def get_enseignant(id_utilisateur):
    enseignant = db.get_or_404(Enseignant, id_utilisateur)
    return  jsonify(enseignant.serialize())


@app.route("/enseignant/add", methods = ["POST"])
def add_enseignant():
    if request.method == "POST": 
        if db.session.query(Enseignant).filter_by(id_utilisateur =request.form["id_utilisateur"]).count() < 1:    
            new_enseignant = Enseignant(id_utilisateur = request.form["id_utilisateur"]
            ,responsabilite_ens = request.form["responsabilite_ens"]
            ,volume_horaire = request.form["volume_horaire"])
            db.session.add(new_enseignant)
            db.session.commit()
        else :
            return jsonify({'error': 'id_utilisateur should be unique'}), 404
        
    return redirect(url_for("get_enseignants"))

@app.route('/enseignant/<id_utilisateur>', methods=['PUT'])
def update_enseignant(id_utilisateur):
    enseignant = db.get_or_404(Enseignant, id_utilisateur)

    if not enseignant:
        return jsonify({'error': 'Enseignant not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        if data.get('responsabilite_ens'):
            enseignant.responsabilite_ens = data['responsabilite_ens']
        if data.get('volume_horaire'):
            enseignant.volume_horaire = data['volume_horaire']

        db.session.commit()
        return jsonify(enseignant.serialize())

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/enseignant/<id_utilisateur>', methods=['DELETE'])
def del_enseignant(id_utilisateur):
    enseignant = Enseignant.query.get(id_utilisateur)
    if not enseignant:
        return jsonify({'error': 'Enseignant not found'}), 404
    try:
        db.session.delete(enseignant)
        db.session.commit()
        return redirect(url_for("get_enseignants"))
    except:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the Enseignant'}), 500

#-------------------Etudiant---------------------------------
@app.route('/etudiants')
def get_etudiants():
    etudiants = Etudiant.query.all()
    return jsonify([etudiant.serialize() for etudiant in etudiants])

@app.route("/etudiant/<id_utilisateur>")
def get_etudiant(id_utilisateur):
    etudiant = db.get_or_404(Etudiant, id_utilisateur)
    return  jsonify(etudiant.serialize())


@app.route("/etudiant/add", methods = ["POST"])
def add_etudiant():
    if request.method == "POST": 
        if db.session.query(Etudiant).filter_by(id_utilisateur =request.form["id_utilisateur"]).count() < 1:    
            new_etudiant = Etudiant(id_utilisateur = request.form["id_utilisateur"]
            ,diplome_etudiant = request.form["diplome_etudiant"]
            ,id_filiere = request.form["id_filiere"])
            if db.session.query(Filiere).filter_by(id_filiere = request.form["id_filiere"]).count() >= 1:
                db.session.add(new_etudiant)
                db.session.commit()
            else:
                return jsonify({'error': 'id_filiere should be existing'}), 404
        else :
            return jsonify({'error': 'id_utilisateur should be unique'}), 404
        
    return redirect(url_for("get_etudiants"))

@app.route('/etudiant/<id_utilisateur>', methods=['PUT'])
def update_etudiant(id_utilisateur):
    etudiant = db.get_or_404(Etudiant, id_utilisateur)

    if not etudiant:
        return jsonify({'error': 'etudiant not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        if data.get('diplome_etudiant'):
            etudiant.diplome_etudiant = data['diplome_etudiant']
        if data.get('id_filiere'):
            etudiant.id_filiere = data['id_filiere']
            if db.session.query(Filiere).filter_by(id_filiere = data.get('id_filiere')).count() < 1:
                return jsonify({'error': 'id_filiere should be existing'}), 405
        db.session.commit()
        return jsonify(etudiant.serialize())

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/etudiant/<id_utilisateur>', methods=['DELETE'])
def del_etudiant(id_utilisateur):
    etudiant = Etudiant.query.get(id_utilisateur)
    if not etudiant:
        return jsonify({'error': 'etudiant not found'}), 404
    try:
        db.session.delete(etudiant)
        db.session.commit()
        return redirect(url_for("get_etudiants"))
    except:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the etudiant'}), 500


#-------------------Filiere-----------------------------------------------

@app.route('/filieres')
def get_filieres():
    filieres = Filiere.query.all()
    return jsonify([filiere.serialize() for filiere in filieres])

@app.route("/filiere/<id_filiere>")
def get_filiere(id_filiere):
    filiere = db.get_or_404(Filiere, id_filiere)
    return  jsonify(filiere.serialize())


@app.route("/filiere/add", methods = ["POST"])
def add_filiere():
    if request.method == "POST": 
        if db.session.query(Filiere).filter_by(id_filiere =request.form["id_filiere"]).count() < 1:    
            new_filiere = Filiere(id_filiere = request.form["id_filiere"]
            ,nom_filiere = request.form["nom_filiere"]
            ,description = request.form["description"]
            ,niveau = request.form["niveau"]
            ,nombre_annee = request.form["nombre_annee"]
            ,id_responsable = request.form["id_responsable"])
            if db.session.query(Enseignant).filter_by(id_utilisateur =request.form["id_responsable"]).count() >= 1:
                db.session.add(new_filiere)
                db.session.commit()
            else:
                return jsonify({'error': 'id_responsable should be existing'}), 404
        else :
            return jsonify({'error': 'id_filiere should be unique'}), 404
        
    return redirect(url_for("get_filieres"))

@app.route('/filiere/<id_filiere>', methods=['PUT'])
def update_filiere(id_filiere):
    filiere = db.get_or_404(Filiere, id_filiere)

    if not filiere:
        return jsonify({'error': 'filiere not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        if data.get('nom_filiere'):
            filiere.nom_filiere = data['nom_filiere']
        if data.get('description'):
            filiere.description = data['description']
        if data.get('niveau'):
            filiere.niveau = data['niveau']
        if data.get('nombre_annee'):
            filiere.nombre_annee = data['nombre_annee']
        if data.get('id_responsable'):
            filiere.id_responsable = data['id_responsable']
            if db.session.query(Enseignant).filter_by(id_utilisateur =data['id_responsable']).count() < 1:
                return jsonify({'error': 'id_responsable should be existing'}), 404
        db.session.commit()
        return jsonify(filiere.serialize())

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/filiere/<id_filiere>', methods=['DELETE'])
def del_filiere(id_filiere):
    filiere = Filiere.query.get(id_filiere)
    if not filiere:
        return jsonify({'error': 'filiere not found'}), 404
    try:
        db.session.delete(filiere)
        db.session.commit()
        return redirect(url_for("get_filieres"))
    except:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the filiere'}), 500


#------------------------------UE------------------------------


@app.route('/ues')
def get_ues():
    ues = UE.query.all()
    return jsonify([ue.serialize() for ue in ues])

@app.route("/ue/<id_ue>")
def get_ue(id_ue):
    ue = db.get_or_404(UE, id_ue)
    return  jsonify(ue.serialize())


@app.route("/ue/add", methods = ["POST"])
def add_ue():
    if request.method == "POST": 
        if db.session.query(UE).filter_by(id_ue =request.form["id_ue"]).count() < 1:    
            new_ue = UE(id_ue = request.form["id_ue"]
            ,id_filiere = request.form["id_filiere"]
            ,libelle_ue = request.form["libelle_ue"]
            ,description = request.form["description"])
            if db.session.query(Filiere).filter_by(id_filiere = request.form["id_filiere"]).count() >=1:
                db.session.add(new_ue)
                db.session.commit()
            else:
                return jsonify({'error': 'id_filiere should be existing'}), 404
            
        else :
            return jsonify({'error': 'id_ue should be unique'}), 404
        
    return redirect(url_for("get_ues"))

@app.route('/ue/<id_ue>', methods=['PUT'])
def update_ue(id_ue):
    ue = db.get_or_404(UE, id_ue)

    if not ue:
        return jsonify({'error': 'ue not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        if data.get('id_filiere'):
            ue.id_filiere = data['id_filiere']
            if db.session.query(Filiere).filter_by(id_filiere = data['id_filiere']).count() < 1:
                return jsonify({'error': 'id_filiere should be existing'}), 404
        if data.get('libelle_ue'):
            ue.libelle_ue = data['libelle_ue']
        if data.get('description'):
            ue.description = data['description']
       
        db.session.commit()
        return jsonify(ue.serialize())

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/ue/<id_ue>', methods=['DELETE'])
def del_ue(id_ue):
    ue = UE.query.get(id_ue)
    if not ue:
        return jsonify({'error': 'ue not found'}), 404
    try:
        db.session.delete(ue)
        db.session.commit()
        return redirect(url_for("get_ues"))
    except:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the ue'}), 500




#-------------------Cours-----------------------------------------------

@app.route('/courss')
def get_courss():
    courss = Cours.query.all()
    return jsonify([cours.serialize() for cours in courss])

@app.route("/cours/<id_cours>")
def get_cours(id_cours):
    cours = db.get_or_404(Cours, id_cours)
    return  jsonify(cours.serialize())


@app.route("/cours/add", methods = ["POST"])
def add_cours():
    if request.method == "POST": 
        if db.session.query(Cours).filter_by(id_cours =request.form["id_cours"]).count() < 1:    
            new_cours = Cours(id_cours = request.form["id_cours"]
            ,id_enseignant = request.form["id_enseignant"]
            ,id_ue = request.form["id_ue"])
            if (db.session.query(Enseignant).filter_by(id_utilisateur =request.form["id_enseignant"]).count() >= 1) and (db.session.query(UE).filter_by(id_ue =request.form["id_ue"]).count() >= 1) :
                db.session.add(new_cours)
                db.session.commit()
            else:
                return jsonify({'error': 'id_enseignant and  id_ue should be existing'}), 404
        else :
            return jsonify({'error': 'id_cours should be unique'}), 404
        
    return redirect(url_for("get_courss"))

@app.route('/cours/<id_cours>', methods=['PUT'])
def update_cours(id_cours):
    cours = db.get_or_404(Cours, id_cours)

    if not cours:
        return jsonify({'error': 'cours not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        if data.get('id_enseignant'):
            cours.id_enseignant = data['id_enseignant']
            if db.session.query(Enseignant).filter_by(id_utilisateur =data['id_enseignant']).count() < 1:
                return jsonify({'error': 'id_enseignant should be existing'}), 404
        if data.get('id_ue'):
            cours.id_ue = data['id_ue']
            if db.session.query(UE).filter_by(id_ue =data['id_ue']).count() < 1:
                return jsonify({'error': 'id_ue should be existing'}), 404
        db.session.commit()
        return jsonify(cours.serialize())

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/cours/<id_cours>', methods=['DELETE'])
def del_cours(id_cours):
    cours = Cours.query.get(id_cours)
    if not cours:
        return jsonify({'error': 'cours not found'}), 404
    try:
        db.session.delete(cours)
        db.session.commit()
        return redirect(url_for("get_courss"))
    except:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the cours'}), 500

#-------------------EDT-----------------------------------------------

@app.route('/edts')
def get_edts():
    edts = EDT.query.all()
    return jsonify([edt.serialize() for edt in edts])

@app.route("/edt/<id_edt>")
def get_edt(id_edt):
    edt = db.get_or_404(EDT, id_edt)
    return  jsonify(edt.serialize())


@app.route("/edt/add", methods = ["POST"])
def add_edt():
    if request.method == "POST": 
        if db.session.query(EDT).filter_by(id_edt =request.form["id_edt"]).count() < 1:    
            date_debut_str = request.form["date_debut"]
            date_fin_str = request.form["date_fin"]
            new_edt = EDT(id_edt = request.form["id_edt"]
            ,id_filiere = request.form["id_filiere"]
            ,id_cours = request.form["id_cours"]
            ,date_debut = parse(date_debut_str)
            ,date_fin = parse(date_fin_str)
            ,type_cours = request.form["type_cours"])
            if (db.session.query(Filiere).filter_by(id_filiere =request.form["id_filiere"]).count() >= 1) and (db.session.query(Cours).filter_by(id_cours =request.form["id_cours"]).count() >= 1) :
                db.session.add(new_edt)
                db.session.commit()
            else:
                return jsonify({'error': 'id_filiere and id_cours should be existing'}), 404
        else :
            return jsonify({'error': 'id_edt should be unique'}), 404
        
    return redirect(url_for("get_edts"))

@app.route('/edt/<id_edt>', methods=['PUT'])
def update_edt(id_edt):
    edt = db.get_or_404(EDT, id_edt)

    if not edt:
        return jsonify({'error': 'edt not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        if data.get('id_filiere'):
            edt.id_filiere = data['id_filiere']
            if db.session.query(Filiere).filter_by(id_filiere =data['id_filiere']).count() < 1:
                return jsonify({'error': 'id_filiere should be existing'}), 404
        if data.get('id_cours'):
            edt.id_cours = data['id_cours']
            if db.session.query(Cours).filter_by(id_cours =data['id_cours']).count() < 1:
                return jsonify({'error': 'id_cours should be existing'}), 404
        if data.get('date_debut'):
            date_debut_str = data['date_debut']
            edt.date_debut = parse(date_debut_str)
        if data.get('date_fin'):
            date_fin_str = data['date_fin']
            edt.date_fin = parse(date_fin_str)
        if data.get('type_cours'):
            edt.type_cours = data['type_cours']
        db.session.commit()
        return jsonify(edt.serialize())

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/edt/<id_edt>', methods=['DELETE'])
def del_edt(id_edt):
    edt = EDT.query.get(id_edt)
    if not edt:
        return jsonify({'error': 'edt not found'}), 404
    try:
        db.session.delete(edt)
        db.session.commit()
        return redirect(url_for("get_edts"))
    except:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the edt'}), 500


#------------Utilisateur-----------------------------------

@app.route('/utilisateurs')
def get_utilisateurs():
    utilisateurs = Utilisateur.query.all()
    return jsonify([utilisateur.serialize() for utilisateur in utilisateurs])


@app.route("/utilisateur/<id_utilisateur>")
def get_utilisateur(id_utilisateur):
    utilisateur = db.get_or_404(Utilisateur, id_utilisateur)
    return  jsonify(utilisateur.serialize())


@app.route("/utilisateur/add", methods = ["POST"])
def add_utilisateur():
    if request.method == "POST": 
        if db.session.query(Utilisateur).filter_by(id_utilisateur =request.form["id_utilisateur"]).count() < 1:    
            new_utilisateur = Utilisateur(id_utilisateur = request.form["id_utilisateur"]
            ,role = request.form["role"]
            ,nom = request.form["nom"]
            ,prenom = request.form["prenom"]
            ,email = request.form["email"]
            ,password = request.form["password"]
            ,tel = request.form["tel"])
            db.session.add(new_utilisateur)
            db.session.commit()
        else :
            return jsonify({'error': 'id_utilisateur should be unique'}), 404
        
    return redirect(url_for("get_utilisateurs"))

@app.route('/utilisateur/<id_utilisateur>', methods=['PUT'])
def update_utilisateur(id_utilisateur):
    utilisateur = db.get_or_404(Utilisateur, id_utilisateur)

    if not utilisateur:
        return jsonify({'error': 'utilisateur not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        if data.get('role'):
            utilisateur.role = data['role']
        if data.get('nom'):
            utilisateur.nom = data['nom']
        if data.get('prenom'):
            utilisateur.prenom = data['prenom']
        if data.get('email'):
            utilisateur.email = data['email']
        if data.get('password'):
            utilisateur.password = data['password']
        if data.get('tel'):
            utilisateur.tel = data['tel']

        db.session.commit()
        return jsonify(utilisateur.serialize())

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/utilisateur/<id_utilisateur>', methods=['DELETE'])
def del_utilisateur(id_utilisateur):
    utilisateur = Utilisateur.query.get(id_utilisateur)
    if not utilisateur:
        return jsonify({'error': 'utilisateur not found'}), 404
    try:
        db.session.delete(utilisateur)
        db.session.commit()
        return redirect(url_for("get_utilisateurs"))
    except:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the utilisateur'}), 500


@app.route("/")
def teste() :
    return "teste reussie"
