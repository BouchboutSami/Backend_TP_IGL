from pydantic import BaseModel

class annonce(BaseModel):
    id_annonce : int
    categorie:str
    type_annonce : str
    surface : int
    description : str
    prix : int
    id_contacts : int
    wilaya :str
    commune :str
    adresse :str
    path_pics :str
    titre : str