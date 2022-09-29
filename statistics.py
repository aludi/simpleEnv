from itertools import product
import csv

class Statistics:
    def __init__(self, model):
        self.model = model
        self.df = []
        self.item_dict = self.init_item_dict()

    def init_item_dict(self):
        C = {}
        valuations = list(product([0, 1], repeat=len(self.model.Ks.domain.keys())))
        keys = list(self.model.Ks.domain.keys())
        for val in valuations:
            new_key = []
            for i in range(0, len(keys)):
                s = keys[i] + "=" + str(val[i])
                new_key.append(s)
            C[tuple(new_key)] = 0
        return C


    def counting(self, cell_item):
        d = {}
        keys = list(self.model.Ks.domain.keys())
        # assume that nothing is found:
        for key in keys:
            d[key] = 0
        for (name, val) in cell_item:
            d[name] = val
        # add d to df
        self.df.append(d)
        # convert d to relevant string format
        l = []
        for key in d.keys():
            l.append(f"{key}={str(d[key])}")
        # then update statistics
        self.item_dict[tuple(l)] += 1



    def collect_statistics(self):
        # print(self.item_dict)
        total = self.model.grid.width * self.model.grid.height
        sum = 0
        for key in self.item_dict.keys():
            print(f"{key}  :  {(self.item_dict[key] / total) * 100}")
            sum += (self.item_dict[key] / total) * 100
        print(sum)
        # convert to csv file
        with open(f"out/{self.model.model}.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.df[0].keys(), extrasaction='ignore')
            writer.writeheader()
            for data in self.df:
                writer.writerow(data)