from webapp.database import db
from sqlalchemy.orm import  relationship


class Enseignant(db.Model):
    __tablename__ = 'enseignant'
    id_utilisateur = db.Column(db.Integer, primary_key=True)
    responsabilite_ens = db.Column(db.String(250))
    volume_horaire = db.Column(db.Integer)

    cours = relationship('Cours', backref='enseignant')

    def serialize(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'responsabilite_ens': self.responsabilite_ens,
            'volume_horaire': self.volume_horaire,

            # 'cours': self.cours,
        }

class Etudiant(db.Model):
    __tablename__ = 'etudiant'
    id_utilisateur = db.Column(db.Integer, primary_key=True)
    diplome_etudiant = db.Column(db.String(250))
    id_filiere = db.Column(db.Integer, db.ForeignKey('filiere.id_filiere'))
    
    def serialize(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'diplome_etudiant': self.diplome_etudiant,
            'id_filiere': self.id_filiere,
        }


class Filiere(db.Model):
    __tablename__ = 'filiere'
    id_filiere = db.Column(db.Integer, primary_key=True)
    nom_filiere = db.Column(db.String(250))
    description = db.Column(db.String(250))
    niveau = db.Column(db.Enum('L', 'M', 'D'))
    nombre_annee = db.Column(db.Integer)
    id_responsable = db.Column(db.Integer, db.ForeignKey('enseignant.id_utilisateur'))

    etudiants = relationship('Etudiant', backref='filiere_participants')
    responsable = relationship('Enseignant', backref='filiere_responsable')
    edt_courses = relationship('EDT', backref='filiere')

    def serialize(self):
        return {
            'id_filiere': self.id_filiere,
            'nom_filiere': self.nom_filiere,
            'description': self.description,
            'niveau': self.niveau,
            'nombre_annee': self.nombre_annee,
            'id_responsable': self.id_responsable,

            # 'etudiants': self.etudiants,
            # 'responsable': self.responsable,
            # 'edt_courses': self.edt_courses,
        }

class UE(db.Model):
    __tablename__ = 'ue'
    id_ue = db.Column(db.Integer, primary_key=True)
    id_filiere = db.Column(db.Integer, db.ForeignKey('filiere.id_filiere'))
    libelle_ue = db.Column(db.String(250))
    description = db.Column(db.String(250))

    cours = relationship('Cours', backref='ue')

    def serialize(self):
        return {
            'id_ue': self.id_ue,
            'id_filiere': self.id_filiere,
            'libelle_ue': self.libelle_ue,
            'description': self.description,
            
            # 'cours': self.cours,
        }


class Cours(db.Model):
    __tablename__ = 'cours'
    id_cours = db.Column(db.Integer, primary_key=True)
    id_enseignant = db.Column(db.Integer, db.ForeignKey('enseignant.id_utilisateur'))
    id_ue = db.Column(db.Integer, db.ForeignKey('ue.id_ue'))

    edt = relationship('EDT', backref='cours')

    def serialize(self):
        return {
            'id_cours': self.id_cours,
            'id_enseignant': self.id_enseignant,
            'id_ue': self.id_ue,
            
            # 'edt': self.edt,
        }


class EDT(db.Model):
    __tablename__ = 'edt'
    id_edt = db.Column(db.Integer, primary_key=True)
    id_filiere = db.Column(db.Integer, db.ForeignKey('filiere.id_filiere'))
    id_cours = db.Column(db.Integer, db.ForeignKey('cours.id_cours'))
    date_debut = db.Column(db.DateTime)
    date_fin = db.Column(db.DateTime)
    type_cours = db.Column(db.Enum('td', 'tp', 'cours'))

    filiere_edt = relationship('Filiere', backref='edt')

    def serialize(self):
        return {
            'id_edt': self.id_edt,
            'id_filiere': self.id_filiere,
            'id_cours': self.id_cours,
            'date_debut': self.date_debut,
            'date_fin': self.date_fin,
            'type_cours': self.type_cours,

            # 'filiere_edt': self.filiere_edt,
        }
    
    #user
class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    id_utilisateur = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(250))
    nom = db.Column(db.String(250))
    prenom = db.Column(db.String(250))
    email = db.Column(db.String(250))
    password = db.Column(db.String(250))
    tel = db.Column(db.String(250))

    def serialize(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'role': self.role,
            'nom': self.nom,
            'prenom': self.prenom,
            'email': self.email,
            'password': self.password,
            'tel': self.tel
        }
    
    
    #note