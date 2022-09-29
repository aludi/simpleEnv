import bn
import model
import server

model_name = "M1"
for model_name in ["M1"]:
    server.server_main_call(model_name)
    #model.SimpleEnv(N=0, width=5, height=2, model=model_name)
    bn.generate_BN(model_name)

