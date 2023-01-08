from pydantic import BaseModel 


class messagerie(BaseModel):
   id_annonce:int 
   id_sender : int
   id_receiver : int
   msg_content : str
   
   def get_messages(self):
    return self.id_annonce