import bn
import model
import server


l = []
for model_name in ["M1", "M2", "M3"]:
    #server.server_main_call(model_name)
    m = model.SimpleEnv(N=2, width=25, height=25, model=model_name)
    for j in range(20):
        m.step()
    m.statistics.collect_statistics()

    l.append((model_name, m.prediction_dict))
    bn.generate_ground_BN(m.Ks)

    #bn.generate_BN(model_name)
print()
print()
print(l)

