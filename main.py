import bn
import model
import server

model_name = "M1"
for model_name in ["M1", "M2"]:
    #server.server_main_call(model_name)
    model.SimpleEnv(N=0, width=50, height=50, model=model_name)
    bn.generate_BN(model_name)

