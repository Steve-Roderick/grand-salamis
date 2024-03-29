#!/usr/bin/env python3
#
#
# Do some softball stats
#
#
import csv
import re
import os
import glob


class Baller(object):
    '''The eater of salamis sticks'''
    B1 = 0
    B2 = 0
    B3 = 0
    HR = 0
    GS = 0
    FC = 0
    XX = 0
    AB = 0
    R = 0
    RBI = 0
    OBP = 0
    SLG = 0
    OPS = 0
    TCD = 0

    def __init__(self, name):
        self.name = name

    def header(self):
        print("| Name       |  1B |  2B |  3B |  HR |  GS |  FC |   X |  AB |   R | RBI |  OBP |  SLG |  OPS |")
        print("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

    def print(self):
        print("| {} | {: >3d} | {: >3d} | {: >3d} | {: >3d} | {: >3d} | {: >3d} | {: >3d} | {: >3d} | {: >3d} | {: >3d} | {:0.2f} | {:0.2f} | {:0.2f} |".format(
            self.name.ljust(10),
            self.B1,
            self.B2,
            self.B3,
            self.HR,
            self.GS,
            self.FC,
            self.XX,
            self.AB,
            self.R,
            self.RBI,
            self.OBP,
            self.SLG,
            self.OPS))


    def header_csv(self):
        print("Name, 1B, 2B, 3B, HR, GS, FC, X, AB, R, RBI, OBP, SLG, OPS")

    def print_csv(self):
        print("{},{},{},{},{},{},{},{},{},{},{},{:0.2f},{:0.2f},{:0.2f}".format(
            self.name,
            self.B1,
            self.B2,
            self.B3,
            self.HR,
            self.GS,
            self.FC,
            self.XX,
            self.AB,
            self.R,
            self.RBI,
            self.OBP,
            self.SLG,
            self.OPS))

    def loadDatum(baller, datum):
        match datum:
            case "1B":
                baller.B1 += 1
            case "2B":
                baller.B2 += 1
            case "3B":
                baller.B3 += 1
            case "HR":
                baller.HR += 1
            case "GS":
                baller.GS += 1
            case "FC":
                baller.FC += 1
            case "X":
                baller.XX += 1
            case _:
                if re.match(r".* R$", datum):
                    cnt = re.findall(r'\d+', datum)
                    baller.R += int(cnt[0])
                    return
                if re.match(r".* RBI$", datum):
                    cnt = re.findall(r'\d+', datum)
                    baller.RBI += int(cnt[0])
                    return
                if re.match(r".* TCD$", datum):
                    cnt = re.findall(r'\d+', datum)
                    baller.TCD += int(cnt[0])
                    return

                print("Ohh no {} {}".format(baller.name, datum))
                exit(0)
        return

    def stats(self):

        # Count AB
        self.AB += self.B1
        self.AB += self.B2
        self.AB += self.B3
        self.AB += self.HR
        self.AB += self.GS
        self.AB += self.FC
        self.AB += self.XX

        # OBP
        self.OBP = (self.AB - self.XX - (self.FC/2.0)) / self.AB

        # SLG
        z = 0.5 * self.FC
        a = 1 * self.B1
        b = 2 * self.B2
        c = 3 * self.B3
        d = 4 * self.HR
        e = 4 * self.GS
        self.SLG = (z + a + b + c + d + e) / self.AB

        # OPS
        self.OPS = self.OBP + self.SLG


def run(team, log):
    header = notes = None
    for f in log:
        fp = f
        with open(fp, 'r') as csvfile:
            datareader = csv.reader(csvfile)

            header = next(datareader)
            notes = next(datareader)
            for row in datareader:
                name = row[0].strip()
                baller = team.get(name)
                if not baller:
                    baller = Baller(name)
                    team[baller.name] = baller

                for col in row[1:]:
                    dp = col.strip()
                    baller.loadDatum(dp)
    return (header, notes)

def team_avg(team):
    b = Baller("Z Team Avg")
    for _, v in team.items():
        b.B1 += v.B1
        b.B2 += v.B2
        b.B3 += v.B3
        b.HR += v.HR
        b.GS += v.GS
        b.FC += v.FC
        b.XX += v.XX
        b.R  += v.R
        b.RBI += v.RBI
    b.stats()
    team[b.name] = b


def report(log, doSort):
    team = {}
    header, notes = run(team, log)

    if not doSort:
        print(header[0])
        print("")
        print(notes[0])
        print("")
    for _, value, in team.items():
        value.stats()

    team_avg(team)

    if doSort:
        lst = sorted(team.items())
    else:
        lst = team.items()

    i = 0
    for _, value in lst:
        if i == 0:
            value.header()
        value.print()
        i = i + 1
    print("")
    print("")


if __name__ == '__main__':

    search = os.path.join("./", "games", "*.csv")
    games = sorted(glob.glob(search), reverse=True)

    print("# Grand Salamis")
    print("")
    # Report season stats cumulative.
    print("# Summer 2023 Totals")
    print("")
    report(games, True)

    # Report each game
    for game in games:
        report([game], False)

    # Legend
    print("### Legend")
    print(" * X denotes did not reach base")

