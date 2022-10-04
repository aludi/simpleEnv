import bn
import model
import server


for model_name in ["M1", "M2", "M3"]:
    #server.server_main_call(model_name)
    m = model.SimpleEnv(N=0, width=25, height=25, model=model_name)
    for j in range(1):
        m.step()
    m.statistics.collect_statistics()
    bn.generate_BN(model_name)

