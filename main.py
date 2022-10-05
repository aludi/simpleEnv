import bn
import model
import server


for model_name in ["M3"]:
    #server.server_main_call(model_name)
    m = model.SimpleEnv(N=2, width=25, height=25, model=model_name)
    for j in range(10):
        m.step()
    m.statistics.collect_statistics()
    bn.generate_ground_BN(m.Ks)
    bn.generate_BN(model_name)

