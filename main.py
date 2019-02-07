from iaas.abstract import IAASManager
if __name__=="__main__":
   im = IAASManager()
   im.call("create_entitya", {"entitya_name": "test", "user_pass":"pass"})

