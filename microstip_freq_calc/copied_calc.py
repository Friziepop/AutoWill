import math


class MicroStripCopiedCalc:
    # consts
    msZofn = 59.9585

    def __init__(self):
        super().__init__()

    def calc(self, er: float, height: float, thickness: float, z0: float, freq: float):
        return self._msCalcWidth(er=er, h=height, t=thickness, z0=z0, f=(freq * 10 ** 9))

    def _msCalcWidth(self, er, h, t, z0, f):
        u = 0.1
        du = 0.5
        v1 = self._getV(er, h, t, u, z0, f)
        u += du
        v2 = self._getV(er, h, t, u, z0, f)
        while v1 * v2 > 0:
            v1 = v2
            u += du
            v2 = self._getV(er, h, t, u, z0, f)
        u2 = u
        u1 = u - du
        u = u1 + (u2 - u1) * 0.381966
        u3 = u
        v3 = abs(self._getV(er, h, t, u, z0, f))
        u = u1 + (u2 - u1) / 1.618034
        u4 = u
        v4 = abs(self._getV(er, h, t, u4, z0, f))
        Zerr = z0 / 10000.0
        while (v3 + v4) > Zerr:
            if v3 > v4:
                u1 = u3
                u3 = u4
                v3 = v4
                u = u1 + (u2 - u1) / 1.618034
                u4 = u
                v4 = abs(self._getV(er, h, t, u, z0, f))
            else:
                u2 = u4
                u4 = u3
                v4 = v3
                u = u1 + (u2 - u1) * 0.381966
                u3 = u
                v3 = abs(self._getV(er, h, t, u, z0, f))
        u = (u1 + u2) / 2
        return u * h

    def _getV(self, er, h, t, u, z, f):
        w = u * h
        msZo = self._msCalcZo(er, h, t, w, f)
        v = msZo - z
        return v

    def _msCalcZo(self, er, h, t, w, f):
        u = w / h
        du1 = 0
        dur = 0
        if t > 0:
            tu = t / h
            du1 = (tu / math.pi) * math.log1p(4.0 * math.e / (tu * self._coth2(math.pow(6.517 * u, 0.5))))
            dur = 0.5 * (1.0 + 1.0 / math.cosh(math.pow(er - 1.0, 0.5))) * du1

        u1 = u + du1
        ur = u + dur
        Zo = self._Zo1(ur) / math.pow(self._msCalcEeff(ur, er), 0.5)
        eff0 = self._msCalcEeff(ur, er) * math.pow(self._Zo1(u1) / self._Zo1(ur), 2.0)
        fn = f * h * 0.0254 / 1.0e9
        p1 = 0.27488 + u * (0.6315 + 0.525 / math.pow(1.0 + 0.0157 * fn, 20.0)) - 0.065683 * math.exp(-8.7513 * u)
        p2 = 0.33622 * (1.0 - math.exp(-0.03442 * er))
        p3 = 0.0363 * math.exp(-4.6 * u) * (1.0 - math.exp(-1.0 * math.pow(fn / 3.87, 4.97)))
        p4 = 2.751 * (1.0 - math.exp(-1.0 * math.pow(er / 15.916, 8.0))) + 1.0
        p = p1 * p2 * math.pow(fn * (0.1844 + p3 * p4), 1.5763)
        msEeff = (eff0 + er * p) / (1.0 + p)
        r1 = 0.03891 * math.pow(er, 1.4)
        r2 = 0.267 * math.pow(u, 7.0)
        r3 = 4.766 * math.exp(-3.228 * math.pow(ur, 0.641))
        r4 = 0.016 + math.pow(0.0514 * er, 4.524)
        r5 = math.pow(fn / 28.843, 12.0)
        r6 = 22.2 * math.pow(ur, 1.92)
        r7 = 1.206 - 0.3144 * math.exp(-r1) * (1.0 - math.exp(-r2))
        r8 = 1.0 + 1.275 * (1.0 - math.exp(-0.004625 * r3 * math.pow(er, 1.674) * math.pow(fn / 18.365, 2.745)))
        r9 = (5.086 * r4 * r5 / (0.3838 + 0.386 * r4)) * (math.exp(-r6) / (1.0 + 1.2992 * r5)) * math.pow(er - 1.0,
                                                                                                          6.0) / (
                     1.0 + 10.0 * math.pow(er - 1.0, 6.0))
        r10 = 0.00044 * math.pow(er, 2.136) + 0.0184
        r11 = math.pow(fn / 19.47, 6.0) / (1.0 + 0.0962 * math.pow(fn / 19.47, 6.0))
        r12 = 1.0 / (1.0 + 0.00245 * u * u)
        r13 = 0.9408 * math.pow(msEeff, r8) - 0.9603
        r14 = (0.9408 - r9) * math.pow(eff0, r8) - 0.9603
        r15 = 0.707 * r10 * math.pow(fn / 12.3, 1.097)
        r16 = 1.0 + 0.0503 * er * er * r11 * (1.0 - math.exp(-1.0 * math.pow(u / 15.0, 6.0)))
        r17 = r7 * (1.0 - 1.1241 * (r12 / r16) * math.exp(-0.026 * math.pow(fn, 1.15656) - r15))
        return Zo * math.pow(r13 / r14, r17)

    def _msCalcEeff(self, u, er):
        a = 1.0 + math.log(
            (math.pow(u, 4.0) + math.pow(u / 52.0, 2.0)) / (math.pow(u, 4.0) + 0.432)) / 49.0 + math.log1p(
            math.pow(u / 18.1, 3)) / 18.7
        b = 0.564 * math.pow((er - 0.9) / (er + 3.0), 0.053)
        ef = (er + 1.0) / 2.0 + ((er - 1) / 2.0) * math.pow((1.0 + 10.0 / u), -1.0 * a * b)
        return ef

    def _Zo1(self, u):
        f = 6.0 + (2.0 * math.pi - 6.0) * math.exp(-1.0 * math.pow((30.666 / u), 0.7528))
        z = MicroStripCopiedCalc.msZofn * math.log(f / u + math.pow(1.0 + 4.0 / (u * u), 0.5))
        return z

    def _coth2(self, x):
        retVal = ((math.exp(x) + math.exp(-x)) / 2.0) / ((math.exp(x) - math.exp(-x)) / 2.0)
        return retVal * retVal
