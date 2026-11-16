#!/usr/bin/env python3
# boxes.py generator "BeeFrameHolder"
# Copy this file to boxes/generators/beekeeping/beeframeholder.py
# (class name BeeFrameHolder).

import math

from boxes import Boxes

try:  # Farbe für Beschriftungen (wird nicht geschnitten)
    from boxes.Color import Color

    ANNOTATION_COLOR = Color.ANNOTATIONS
except Exception:
    ANNOTATION_COLOR = [1.0, 0.0, 0.0]

try:  # neuere boxes.py-Versionen: BoolArg() als Typ
    from boxes import BoolArg

    boolarg = BoolArg()
except ImportError:  # ältere Versionen: Funktion boolarg
    from boxes import boolarg


class BeeFrameHolder(Boxes):
    """Rahmen zum Einhängen von Rähmchen aus Begattungskästchen in eine Beute,
    Enden variabel, optionale Ständer"""

    ui_group = "Beekeeping"

    # Haltestege (Standardeinstellung "tabs" = Breite eines Stegs in mm): nur waagerechte
    # Kanten ab dieser Länge ohne Zinken/Einkerbungen bekommen Stege (Zinken, Einkerbungen und
    # Ohren bleiben sauber); ab TAB_TWO_EDGE zwei Stege, sonst einen in der Mitte
    TAB_MIN_EDGE = 20.0
    TAB_TWO_EDGE = 100.0

    # Untere Verstrebung an den Ständern:
    # Abstand der Verstrebung von der Außenkante der Ständer und Abstand ihrer Unterkante
    # vom unteren Rand der Ständer (mm)
    STAND_BRACE_OFFSET = 2.5
    STAND_BRACE_BOTTOM = 2.5

    def __init__(self):
        Boxes.__init__(self)
        add = self.argparser.add_argument

        # Option "labels" von boxes.py übernehmen; falls es sie nicht gibt, selbst anlegen
        if not any("--labels" in a.option_strings for a in self.argparser._actions):
            add(
                "--labels",
                action="store",
                type=boolarg,
                default=True,
                help="Maße als Beschriftung im ersten Seitenteil",
            )

        add(
            "--breite",
            action="store",
            type=float,
            default=81.0,
            help="Innenbreite zwischen den Seitenwänden (mm)",
        )
        add(
            "--laenge",
            action="store",
            type=float,
            default=470.0,
            help="Gesamtlänge der Seitenwände inkl. Ohren (mm)",
        )
        add(
            "--hoehe",
            action="store",
            type=float,
            default=40.0,
            help="Höhe des Rahmens (mm), ohne Ständer",
        )
        add(
            "--finger_width",
            action="store",
            type=float,
            default=2.0,
            help="Breite der Zinken in Vielfachen der Materialdicke",
        )

        add(
            "--ends",
            action="store",
            type=str,
            default="hang",
            choices=["hang", "hook"],
            help="Enden der Seitenwände: hang = Ohren an beiden Enden, "
            "hook = Haken links, rechts stumpf",
        )
        add(
            "--hang_height",
            action="store",
            type=float,
            default=10.0,
            help="Höhe der Aufhängung (Ohren) in mm; bei ends = hook die Höhe des Stegs "
            "über der Lücke des Hakens",
        )
        add(
            "--hang_inset",
            action="store",
            type=float,
            default=20.0,
            help="Ohrenlänge. Abstand der Außenseite von Stirn-/Rückwand zum äußeren Ende (mm), "
            "nur bei ends = hang",
        )

        # Untermenü "Abstandshalter"
        nadd = self.argparser.add_argument_group("Abstandshalter").add_argument
        nadd(
            "--notch_width",
            action="store",
            type=float,
            default=25.0,
            help="Breite Rähmchen zum Einhängen (mm)",
        )
        nadd(
            "--notch_pitch",
            action="store",
            type=float,
            default=35.0,
            help="Abstand von Mitte zu Mitte der Rähmchen (mm)",
        )
        nadd(
            "--notch_depth",
            action="store",
            type=float,
            default=10.0,
            help="Tiefe der Einkerbungen (mm)",
        )
        nadd(
            "--notch_radius",
            action="store",
            type=float,
            default=1.0,
            help="Radius der Abrundung an der Oberseite der Einkerbungen (mm)",
        )
        nadd(
            "--notch_spacing",
            action="store",
            type=float,
            default=5.0,
            help="Mindestabstand an beiden Enden von der Innenseite der Stirnwand (mm); ",
        )
        nadd(
            "--notch_continuous",
            action="store",
            type=boolarg,
            default=False,
            help="eine durchgehende vertiefte Leiste ohne Einkerbungen",
        )

        # Untermenü "Settings for Hook"
        hadd = self.argparser.add_argument_group("Settings for Hook").add_argument
        hadd(
            "--hook_width",
            action="store",
            type=float,
            default=9.5,
            help="Breite des Hakens am äußeren Ende (mm)",
        )
        hadd(
            "--hook_height",
            action="store",
            type=float,
            default=30.0,
            help="Länge des Hakens nach unten, gemessen ab Oberkante des Rahmens (mm)",
        )
        hadd(
            "--hook_gap",
            action="store",
            type=float,
            default=20.5,
            help="Lücke zwischen Haken und Außenseite der Stirnwand (mm)",
        )
        hadd(
            "--hook_radius",
            action="store",
            type=float,
            default=2.5,
            help="Abrundung der äußeren Ecken des Hakens (mm)",
        )
        hadd(
            "--hook_inner_radius",
            action="store",
            type=float,
            default=1.0,
            help="Abrundung der inneren unteren Ecke des Hakens (mm)",
        )

        # Untermenü "Settings for Stand"
        sadd = self.argparser.add_argument_group("Settings for Stand").add_argument
        sadd(
            "--stands",
            action="store",
            type=boolarg,
            default=False,
            help="Ständer an den Seitenwänden (zieht Stirn- und Rückwand nach unten). "
            "Bei ends = hook nur der linke Ständer",
        )
        sadd(
            "--stand_top_width",
            action="store",
            type=float,
            default=50.0,
            help="Breite der Ständer oben, am Rahmen (mm), gemessen ab der Außenseite der Stirn-/Rückwand",
        )
        sadd(
            "--stand_bottom_width",
            action="store",
            type=float,
            default=30.0,
            help="Breite der Ständer unten (mm), gemessen ab der Außenseite der Stirn-/Rückwand",
        )
        sadd(
            "--stand_height",
            action="store",
            type=float,
            default=50.0,
            help="Höhe der Ständer zusätzlich zur Rahmenhöhe (mm)",
        )
        sadd(
            "--stand_radius",
            action="store",
            type=float,
            default=1.0,
            help="Abrundung der unteren Ecken der Ständer (mm)",
        )
        sadd(
            "--stand_brace",
            action="store",
            type=boolarg,
            default=True,
            help="Verstrebung auch unten an den Ständern (nur wenn Ständer aktiv)",
        )
        sadd(
            "--brace_height",
            action="store",
            type=float,
            default=10.0,
            help="Höhe der senkrechten Verstrebungen an den Ständern (mm). Bei ends = hook "
            "automatisch gleich hang_height",
        )
        sadd(
            "--brace_tenon_inset",
            action="store",
            type=float,
            default=3.0,
            help="Zapfen der senkrechten Verstrebungen an den Ständern: Abstand des Zapfens "
            "(und des Lochs in den Seitenwänden) vom oberen und vom unteren Rand der Leiste "
            "in mm, der Zapfen ist also insgesamt 2 x brace_tenon_inset schmäler als die Leiste",
        )
        sadd(
            "--endwall_extension",
            action="store",
            type=float,
            default=20.0,
            help="Stirn- und Rückwand bei aktiven Ständern weiter nach unten ziehen (mm)",
        )

    # ------------------------------------------------------------------
    def endLengths(self):
        """Länge der beiden Enden (links, rechts): äußeres Ende bis Innenseite der
        Stirn-/Rückwand."""
        t = self.thickness
        if self.ends == "hook":
            return self.hook_width + self.hook_gap + t, t
        return self.hang_inset + t, self.hang_inset + t

    def standSides(self):
        """Ständer (links, rechts). Bei ends = hook gibt es nur den linken Ständer."""
        return self.stands, self.stands and self.ends != "hook"

    def endKinds(self):
        """Form der Enden (links, rechts): ear = Ohr, hook = Haken, blunt = stumpf."""
        return ("hook", "blunt") if self.ends == "hook" else ("ear", "ear")

    def earHeight(self):
        """Höhe des Stegs am Ende (Ohr bzw. Steg über der Lücke des Hakens)."""
        return self.hang_height

    def braceDepth(self):
        """Abstand der Oberkante der waagrechten Verstrebung von der Oberkante der Ohren:
        immer mittig im Ohr, also (hang_height - Materialdicke) / 2."""
        return (self.earHeight() - self.thickness) / 2.0

    def checkParams(self):
        t = self.thickness
        if self.ends == "hook":
            # Haken: Höhe der senkrechten Verstrebungen passend zum Steg über der Lücke
            self.brace_height = self.hang_height
        l0, l1 = self.endLengths()
        T = self.laenge - l0 - l1
        if T <= 0:
            raise ValueError("laenge ist zu kurz für die Enden und Stirn-/Rückwand")
        ear_h = self.earHeight()
        if not 0 < ear_h < self.hoehe:
            raise ValueError("hang_height muss größer 0 und kleiner als hoehe sein")
        if self.ends == "hook":
            if self.hook_width <= 0 or self.hook_gap <= 0:
                raise ValueError("hook_width und hook_gap müssen größer 0 sein")
            if not self.hang_height < self.hook_height < self.hoehe:
                raise ValueError(
                    "hook_height muss größer als hang_height und kleiner als hoehe sein"
                )
            if self.hook_radius < 0 or self.hook_inner_radius < 0:
                raise ValueError("Die Abrundungen des Hakens dürfen nicht negativ sein")
            if self.hook_radius + self.hook_inner_radius > self.hook_width:
                raise ValueError("Die Abrundungen sind zu groß für hook_width")
            if 2 * self.hook_radius > self.hook_height:
                raise ValueError("hook_radius ist zu groß für hook_height")
            if self.hook_inner_radius > self.hook_height - self.hang_height:
                raise ValueError(
                    "hook_inner_radius ist zu groß für hook_height - hang_height"
                )
        # Die waagrechte Verstrebung liegt mittig im Ohr; der Abstand zur Ober- und Unterkante
        # des Ohrs muss mindestens 2 mm betragen
        if self.braceDepth() < 2.0 - 1e-9:
            raise ValueError(
                "Die waagrechte Verstrebung passt nicht in die Höhe der Ohren: hang_height "
                "muss mindestens Materialdicke + 4 mm sein (%.1f mm), damit sie mittig liegt "
                "und mindestens 2 mm Abstand zur Kante hat" % (t + 4.0)
            )
        for length, stand in self.braceEnds():
            if length < 3.0:
                raise ValueError(
                    "Die Ohren sind zu kurz für die waagrechte Verstrebung"
                )
            if self.plateFingers(length)[0] < 1.0:
                raise ValueError(
                    "Die Zinken der waagrechten Verstrebung sind zu schmal: "
                    "finger_width vergrößern oder die Ohren verlängern"
                )
            if self.plateEndFingers(stand)[0] < 1.0:
                raise ValueError(
                    "Die Zinken der waagrechten Verstrebung zur Stirn-/Rückwand sind zu "
                    "schmal: finger_width vergrößern"
                )
        if self.stands:
            if self.stand_height < self.endwall_extension:
                raise ValueError(
                    "stand_height muss mindestens so groß sein wie endwall_extension"
                )
            n_stands = sum(self.standSides())
            if n_stands * self.stand_top_width > T:
                raise ValueError("Die Ständer sind zu breit für die Seitenwand")
            if self.stand_top_width <= 0 or self.stand_bottom_width <= 0:
                raise ValueError("Die Ständerbreiten müssen größer 0 sein")
            if self.stand_brace:
                if (
                    self.brace_tenon_inset < 0
                    or 2 * self.brace_tenon_inset >= self.brace_height
                ):
                    raise ValueError("brace_tenon_inset ist zu groß für brace_height")
                if self.STAND_BRACE_BOTTOM + self.brace_height > self.stand_height - 2:
                    raise ValueError(
                        "Die untere Verstrebung passt nicht in die Ständerhöhe: "
                        "5 mm + brace_height muss kleiner als stand_height - 2 sein"
                    )
                if (
                    self.STAND_BRACE_OFFSET + t
                    > min(self.stand_top_width, self.stand_bottom_width) - 1
                ):
                    raise ValueError(
                        "Die untere Verstrebung passt nicht in den Ständer: "
                        "5 mm + Materialdicke muss kleiner als die Ständerbreite - 1 sein"
                    )

    # ------------------------------------------------------------------
    def jointSegments(self, stand):
        """Zinkenverbindung Seitenwand <-> Stirn-/Rückwand über die volle Höhe.
        Liefert (z_unten, Segmente von unten nach oben). 'E' = Zinken der Stirn-/Rückwand,
        'S' = Zinken der Seitenwand. Unten ist immer 'E', oben immer 'S'."""
        t = self.thickness
        zj0 = -self.endwall_extension if stand else 0.0
        Lj = self.hoehe - zj0
        n = max(1, int(round(Lj / (2 * self.finger_width * t))))
        w = Lj / (2 * n)
        segs = []
        for k in range(2 * n):
            zb = zj0 + k * w
            segs.append((zb, zb + w, "E" if k % 2 == 0 else "S"))
        return zj0, segs

    # ------------------------------------------------------------------
    def endJoint(self, x1, segs, kind):
        """Ein Ende der Seitenwand von unten nach oben: Zinken und Ohr, Haken oder
        stumpfes Ende. Das Ende wird im Bezugssystem des rechten Endes beschrieben
        (x wächst zum äußeren Ende, das bei x = y liegt); das linke Ende wird
        gespiegelt. kind: "ear", "hook" oder "blunt".
        Liefert (Punkte (x, z, Radius), Löcher). Im Bereich von Ohr bzw. Haken
        werden die Lücken zu geschlossenen Löchern, durch die die Zinken der
        Stirn-/Rückwand ragen."""
        t = self.thickness
        x2 = x1 + t
        eps = 1e-6
        pts, holes = [], []

        if kind == "blunt":
            # Stumpf: Zinken bis zur Außenseite der Stirnwand, kein Ohr.
            for zb, zt, typ in segs:
                if typ == "S":
                    pts += [(x1, zb, 0), (x2, zb, 0), (x2, zt, 0), (x1, zt, 0)]
            return pts, holes

        ze = self.hoehe - self.earHeight()
        if kind == "hook":
            # Unterkante des Stegs nach außen bis zur Lücke, dann am Haken
            # nach unten, an der Unterseite nach außen und außen wieder hoch.
            zhb = self.hoehe - self.hook_height
            out = [
                (x2 + self.hook_gap, ze, 0),
                (x2 + self.hook_gap, zhb, self.hook_inner_radius),
                (self.laenge, zhb, self.hook_radius),
            ]
            top = (self.laenge, self.hoehe, self.hook_radius)
        else:
            x3 = x2 + self.hang_inset
            out = [(x3, ze, 0)]
            top = (x3, self.hoehe, 0)

        ear = False
        for zb, zt, typ in segs:
            if ear:
                if typ == "E":
                    holes.append((x1, zb, x2, zt))
                continue
            if zt <= ze + eps:  # komplett unterhalb des Stegs
                if typ == "S":
                    if zt >= ze - eps:  # Zinken endet genau an der Unterkante des Stegs
                        pts += [(x1, zb, 0), (x2, zb, 0), (x2, ze, 0)] + out
                        ear = True
                    else:
                        pts += [(x1, zb, 0), (x2, zb, 0), (x2, zt, 0), (x1, zt, 0)]
            elif zb < ze - eps:  # Segment liegt über der Unterkante des Stegs
                if typ == "S":
                    pts += [(x1, zb, 0), (x2, zb, 0), (x2, ze, 0)] + out
                else:
                    pts += [(x1, zt, 0), (x2, zt, 0), (x2, ze, 0)] + out
                ear = True
            else:  # beginnt genau an der Unterkante des Stegs
                pts += [(x1, ze, 0)] + out
                ear = True
                if typ == "E":
                    holes.append((x1, zb, x2, zt))
        pts.append(top)
        return pts, holes

    def endPolyline(self, kind, l, stand):
        """Ein komplettes Ende der Seitenwand von unten nach oben im Bezugssystem
        des rechten Endes: Ständer (falls aktiv), Zinken und Ohr/Haken/stumpf.
        l = Länge des Endes bis zur Innenseite der Stirn-/Rückwand,
        stand = Ständer an diesem Ende.
        Liefert (Punkte (x, z, Radius), Löcher)."""
        t = self.thickness
        x1 = self.laenge - l
        zj0, segs = self.jointSegments(stand)
        sh = self.stand_height

        R = []
        if stand:
            # Außenkante des Ständers bündig mit der Außenseite der Stirn-/Rückwand:
            # zusammengebaut ergibt das eine durchgehende, glatte Wand ohne Absatz.
            xo = x1 + t
            R += [
                (xo - self.stand_top_width, 0, 0),
                (xo - self.stand_bottom_width, -sh, self.stand_radius),
                (xo, -sh, self.stand_radius),
                (xo, zj0, 0),
                (x1, zj0, 0),  # Auflage für die Unterkante der Stirn-/Rückwand
            ]
        else:
            R += [(x1, 0, 0)]

        right, holes = self.endJoint(x1, segs, kind)

        if kind in ("ear", "hook"):
            # Löcher für die Zinken der waagrechten Verstrebung (Ohr bzw. Steg über dem Haken);
            # u = Abstand von der Außenseite der Stirn-/Rückwand nach außen
            zt = self.hoehe - self.braceDepth()
            for u0, u1 in self.plateFingers(l - t)[1]:
                holes.append((x1 + t + u0, zt - t, x1 + t + u1, zt))
        return R + right, holes

    # ------------------------------------------------------------------
    def notchLayout(self, l0, l1):
        """Prüft die Einkerbungs-Parameter und liefert die linken Kanten der Einkerbungen
        (x-Positionen von der Stirnseite aus). l0 und l1 sind die Längen des linken und
        des rechten Endes bis zur Innenseite der Stirn-/Rückwand.
        Es werden immer so viele Einkerbungen gemacht, wie hineinpassen; die Gruppe sitzt
        mittig zwischen Stirn- und Rückwand."""
        nw, pitch, d = self.notch_width, self.notch_pitch, self.notch_depth
        sp, r = self.notch_spacing, self.notch_radius
        T = (
            self.laenge - l0 - l1
        )  # Länge zwischen den Innenseiten von Stirn- und Rückwand

        if r > d or 2 * r > nw:
            raise ValueError("notch_radius ist zu groß für Tiefe/Breite der Einkerbung")
        if pitch <= 0:
            raise ValueError("notch_pitch muss größer 0 sein")
        if not self.notch_continuous and pitch - nw < 2 * r:
            raise ValueError(
                "notch_pitch ist zu klein: mindestens notch_width + 2 * notch_radius = %.1f mm"
                % (nw + 2 * r)
            )
        if sp < r:
            raise ValueError(
                "notch_spacing muss mindestens so groß sein wie notch_radius"
            )

        # So viele wie passen, als Gruppe mittig zwischen Stirn- und Rückwand
        if T - 2 * sp - nw < -1e-6:
            return []
        n = int((T - 2 * sp - nw + 1e-6) // pitch) + 1
        span = (n - 1) * pitch + nw
        start = l0 + (T - span) / 2.0
        return [start + i * pitch for i in range(n)]

    def notchCount(self, l0, l1):
        return len(self.notchLayout(l0, l1))

    def notchPoints(self, l0, l1):
        """Einkerbungen oben, von rechts (Rückseite) nach links (Stirnseite).
        Bei notch_continuous eine einzige durchgehende Vertiefung ohne Spitzen."""
        nw, d, r = self.notch_width, self.notch_depth, self.notch_radius
        starts = self.notchLayout(l0, l1)
        if not starts:
            return []
        if self.notch_continuous:
            spans = [(starts[0], starts[-1] + nw)]
        else:
            spans = [(a, a + nw) for a in starts]
        pts = []
        for a, b in reversed(spans):  # a = linke Kante, b = rechte Kante
            pts += [
                (b, self.hoehe, r),
                (b, self.hoehe - d, 0),
                (a, self.hoehe - d, 0),
                (a, self.hoehe, r),
            ]
        return pts

    # ------------------------------------------------------------------
    def tabEdge(self, length):
        """Länge einer geraden Kante, bei langen Kanten als (Länge, Anzahl Stege)."""
        tabs = getattr(self, "tabs", 0)
        if tabs and length >= max(self.TAB_MIN_EDGE, 10 * tabs):
            return (length, 2 if length >= self.TAB_TWO_EDGE else 1)
        return length

    def cleanPolygon(self, pts):
        """Doppelte und auf einer Geraden liegende Punkte entfernen."""
        res = []
        for p in pts:
            if res and abs(p[0] - res[-1][0]) < 1e-9 and abs(p[1] - res[-1][1]) < 1e-9:
                res[-1] = (p[0], p[1], max(p[2], res[-1][2]))
            else:
                res.append(tuple(p))
        if (
            len(res) > 1
            and abs(res[0][0] - res[-1][0]) < 1e-9
            and abs(res[0][1] - res[-1][1]) < 1e-9
        ):
            last = res.pop()
            res[0] = (res[0][0], res[0][1], max(res[0][2], last[2]))
        i = 0
        while i < len(res) and len(res) > 3:
            a, b, c = res[i - 1], res[i], res[(i + 1) % len(res)]
            cross = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
            dot = (b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1])
            if abs(cross) < 1e-9 and dot > 0:
                del res[i]
            else:
                i += 1
        # Startpunkt muss eine scharfe Ecke sein
        start = next((k for k, p in enumerate(res) if p[2] == 0), 0)
        return res[start:] + res[:start]

    def drawPolygon(self, pts, tab_ok=None):
        """Zeichnet ein geschlossenes Polygon (gegen den Uhrzeigersinn).
        pts: Liste von (x, z, Radius). Ecken mit Radius > 0 werden abgerundet.
        tab_ok(p0, p1): darf die Kante von p0 nach p1 Haltestege bekommen (Standard: keine)."""
        pts = self.cleanPolygon(pts)
        n = len(pts)
        lens, angs = [], []
        for i in range(n):
            x0, z0, _ = pts[i]
            x1, z1, _ = pts[(i + 1) % n]
            lens.append(math.hypot(x1 - x0, z1 - z0))
            angs.append(math.degrees(math.atan2(z1 - z0, x1 - x0)))
        turns = []
        for i in range(n):
            j = (i + 1) % n
            turn = (angs[j] - angs[i] + 180.0) % 360.0 - 180.0
            r = pts[j][2]
            if r > 0 and abs(turn) > 1e-6:
                d = r * math.tan(math.radians(abs(turn)) / 2.0)
                lens[i] -= d
                lens[j] -= d
                turns.append((turn, r))
            else:
                turns.append(turn)
        args = []
        for i, (length, turn) in enumerate(zip(lens, turns)):
            if length < -1e-6:
                raise ValueError("Abrundung ist zu groß für eine der Kanten")
            length = max(length, 0.0)
            if tab_ok and tab_ok(pts[i], pts[(i + 1) % n]):
                length = self.tabEdge(length)
            args += [length, turn]
        self.ctx.save()
        self.moveTo(pts[0][0], pts[0][1], angs[0])
        self.polyline(*args)
        self.ctx.stroke()
        self.ctx.restore()

    # ------------------------------------------------------------------
    def sideWall(self, move=None, info=False):
        t = self.thickness
        l0, l1 = (
            self.endLengths()
        )  # links, rechts: äußeres Ende -> Innenseite Stirnwand
        kind0, kind1 = self.endKinds()
        stand0, stand1 = self.standSides()
        sh = self.stand_height if self.stands else 0.0

        tw, th = self.laenge, self.hoehe + sh
        if self.beginPart(tw, th, move):
            return

        # Rechtes Ende von unten nach oben; das linke Ende wird im gleichen
        # Bezugssystem aufgebaut und anschließend gespiegelt.
        R1, holes1 = self.endPolyline(kind1, l1, stand1)
        R0, holes0 = self.endPolyline(kind0, l0, stand0)

        mirror = lambda p: (self.laenge - p[0], p[1], p[2])
        poly = R1 + self.notchPoints(l0, l1) + [mirror(p) for p in reversed(R0)]
        # Haltestege nur auf den unteren, waagerechten Kanten (Rahmenunterkante, Standfüße)
        self.drawPolygon(
            [(x, z + sh, r) for x, z, r in poly],
            tab_ok=lambda a, b: abs(a[1] - b[1]) < 1e-9 and a[1] <= sh + 1e-9,
        )

        # Löcher für die Zinken der Stirn-/Rückwand im Bereich von Ohr bzw. Haken
        for hx1, hz0, hx2, hz1 in holes1:
            self.rectangularHole(
                (hx1 + hx2) / 2, (hz0 + hz1) / 2 + sh, hx2 - hx1, hz1 - hz0
            )
        for hx1, hz0, hx2, hz1 in holes0:
            ax1, ax2 = self.laenge - hx2, self.laenge - hx1
            self.rectangularHole(
                (ax1 + ax2) / 2, (hz0 + hz1) / 2 + sh, ax2 - ax1, hz1 - hz0
            )

        if self.stands and self.stand_brace:
            zc = (
                self.STAND_BRACE_BOTTOM + self.brace_height / 2.0
            )  # ab Ständer-Unterkante
            centers = []
            if stand0:
                centers.append(l0 - t + self.STAND_BRACE_OFFSET + t / 2.0)
            if stand1:
                centers.append(self.laenge - l1 + t - self.STAND_BRACE_OFFSET - t / 2.0)
            for cx in centers:
                self.rectangularHole(
                    cx, zc, t, self.brace_height - 2 * self.brace_tenon_inset
                )
        if info and getattr(self, "labels", True):
            self.writeLabels()
        self.move(tw, th, move)

    # ------------------------------------------------------------------
    def drawLine(self, pts):
        """Zeichnet einen offenen Linienzug mit scharfen Ecken. pts: Liste von (x, z)."""
        res = []
        for p in pts:
            if (
                not res
                or abs(p[0] - res[-1][0]) > 1e-9
                or abs(p[1] - res[-1][1]) > 1e-9
            ):
                res.append(p)
        k = 1
        while k < len(res) - 1:  # Punkte auf einer Geraden entfernen
            a, b, c = res[k - 1], res[k], res[k + 1]
            cross = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
            dot = (b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1])
            if abs(cross) < 1e-9 and dot > 0:
                del res[k]
            else:
                k += 1
        if len(res) < 2:
            return
        lens, angs = [], []
        for a, b in zip(res, res[1:]):
            lens.append(math.hypot(b[0] - a[0], b[1] - a[1]))
            angs.append(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])))
        args = []
        for j, length in enumerate(lens):
            args.append(self.tabEdge(length))
            if j < len(lens) - 1:
                args.append((angs[j + 1] - angs[j] + 180.0) % 360.0 - 180.0)
        self.ctx.save()
        self.moveTo(res[0][0], res[0][1], angs[0])
        self.polyline(*args)
        self.ctx.stroke()
        self.ctx.restore()

    def braceEnds(self):
        """Waagrechte Verstrebungen: je Ohr bzw. Haken eine, als Liste von (Länge, Ständer).
        Die Länge wird ab der Außenseite der Stirn-/Rückwand bis zum äußeren Ende gemessen,
        Ständer sagt, ob die Stirn-/Rückwand an diesem Ende verlängert ist."""
        t = self.thickness
        l0, l1 = self.endLengths()
        kind0, kind1 = self.endKinds()
        stand0, stand1 = self.standSides()
        res = []
        if kind0 in ("ear", "hook"):
            res.append((l0 - t, stand0))
        if kind1 in ("ear", "hook"):
            res.append((l1 - t, stand1))
        return res

    def plateEndFingers(self, stand):
        """Zinken der waagrechten Verstrebung zur Stirn-/Rückwand, entlang der Innenbreite.
        Die Zinkenbreite richtet sich nach der Verzahnung der Seitenwand (jointSegments);
        Muster: Lücke, Zinken, Lücke, ..., Lücke. Liefert (Zinkenbreite, [(u0, u1), ...])
        mit u = Abstand von der Innenseite der Seitenwand."""
        segs = self.jointSegments(stand)[1]
        wj = segs[0][1] - segs[0][0]
        n = max(1, int(round((self.breite / wj - 1.0) / 2.0)))
        w = self.breite / (2 * n + 1)
        return w, [((2 * k + 1) * w, (2 * k + 2) * w) for k in range(n)]

    def plateFingers(self, length):
        """Zinken der waagrechten Verstrebung entlang der Ohrlänge. Muster: Lücke, Zinken,
        Lücke, ..., Lücke (die Löcher in der Seitenwand bleiben ringsum geschlossen).
        Liefert (Zinkenbreite, [(u0, u1), ...]) mit u = Abstand von der Stirn-/Rückwand."""
        fw = self.finger_width * self.thickness
        n = max(1, int(round((length / fw - 1.0) / 2.0)))
        w = length / (2 * n + 1)
        return w, [((2 * k + 1) * w, (2 * k + 2) * w) for k in range(n)]

    def earPlate(self, length, stand=False, move=None):
        """Waagrechte Verstrebung im Ohr: flache Platte (Länge = Ohrlänge, Breite = Außenbreite
        des Rahmens). An den beiden langen Seiten Zinken, die durch Löcher in den Seitenwänden
        ragen, und an der Kante zur Stirn-/Rückwand Zinken (Breite wie bei der Verzahnung der
        Seitenwand), die durch Schlitze in der Stirn-/Rückwand ragen und innen bündig
        abschließen. Das äußere Ende schließt bündig mit dem Ohr ab. Die Platte verhindert,
        dass sich die beiden Seitenwände gegeneinander wie ein Parallelogramm verschieben.
        Bezugssystem: y = t ist die Plattenkante an der Stirn-/Rückwand, y = 0 die Zinkenspitze."""
        t = self.thickness
        W = self.breite + 2 * t
        tw, th = W, length + t
        if self.beginPart(tw, th, move):
            return
        # Kante zur Stirn-/Rückwand (von links nach rechts) mit Zinken nach unten
        B = [(t, t, 0)]
        for u0, u1 in self.plateEndFingers(stand)[1]:
            B += [(t + u0, t, 0), (t + u0, 0, 0), (t + u1, 0, 0), (t + u1, t, 0)]
        B.append((W - t, t, 0))
        # rechte Seite von unten nach oben mit Zinken in die Seitenwand
        R = [(W - t, t, 0)]
        for u0, u1 in self.plateFingers(length)[1]:
            R += [
                (W - t, t + u0, 0),
                (W, t + u0, 0),
                (W, t + u1, 0),
                (W - t, t + u1, 0),
            ]
        R.append((W - t, t + length, 0))
        mirror = lambda p: (W - p[0], p[1], p[2])
        far = t + length  # äußere Kante der Platte (bündig mit dem Ende des Ohrs)
        self.drawPolygon(
            B + R[1:] + [mirror(p) for p in reversed(R)],
            tab_ok=lambda a, b: abs(a[1] - far) < 1e-9 and abs(b[1] - far) < 1e-9,
        )
        self.move(tw, th, move)

    def braceStack(self, n, move=None):
        """n senkrechte Verstrebungen (an den Ständern) übereinander mit gemeinsamen langen
        Kanten (der Laser schneidet
        jede lange Kante nur einmal). Senkrecht stehende Leisten mit Zapfen an beiden Enden:
        Zapfen (Länge = Materialdicke) oben und unten je brace_tenon_inset schmäler.

        Die Linien sind offene Linienzüge: boxes.py korrigiert den Burn nur seitlich der
        Schnittrichtung (rechts). Deshalb liegt das Material immer links der Schnittrichtung,
        und die senkrechten Kanten (Schulter, Zapfenspitze) werden um burn nach außen gesetzt."""
        t = self.thickness
        hb = self.brace_height
        i = self.brace_tenon_inset
        bn = self.burn
        W = self.breite + 2 * t
        tw, th = W, n * hb
        if self.beginPart(tw, th, move):
            return
        for k in range(n + 1):  # gemeinsame lange Kanten
            self.drawLine([(t - bn, k * hb), (W - t + bn, k * hb)])
        for k in range(n):
            z0 = k * hb
            # linker Zapfen, von oben nach unten
            self.drawLine(
                [
                    (t - bn, z0 + hb),
                    (t - bn, z0 + hb - i),
                    (-bn, z0 + hb - i),
                    (-bn, z0 + i),
                    (t - bn, z0 + i),
                    (t - bn, z0),
                ]
            )
            # rechter Zapfen, von unten nach oben
            self.drawLine(
                [
                    (W - t + bn, z0),
                    (W - t + bn, z0 + i),
                    (W + bn, z0 + i),
                    (W + bn, z0 + hb - i),
                    (W - t + bn, z0 + hb - i),
                    (W - t + bn, z0 + hb),
                ]
            )
        self.move(tw, th, move)

    # ------------------------------------------------------------------
    def endWall(self, move=None, stand=False, kind="ear"):
        t = self.thickness
        W = self.breite + 2 * t
        zj0, segs = self.jointSegments(stand)
        tw, th = W, self.hoehe - zj0
        if self.beginPart(tw, th, move):
            return

        R = [(W, zj0, 0)]
        for zb, zt, typ in segs:
            if typ == "S":
                R += [(W, zb, 0), (W - t, zb, 0), (W - t, zt, 0)]
                if zt < self.hoehe - 1e-9:
                    R.append((W, zt, 0))
        mirror = lambda p: (W - p[0], p[1], p[2])
        poly = R + [mirror(p) for p in reversed(R)]
        self.drawPolygon(
            [(x, z - zj0, r) for x, z, r in poly],
            tab_ok=lambda a, b: (
                abs(a[1] - b[1]) < 1e-9
            ),  # Haltestege: obere/untere Kante
        )
        if kind in ("ear", "hook"):
            # Schlitze für die Zinken der waagrechten Verstrebung (liegt außen an der Wand)
            zc = self.hoehe - self.braceDepth() - t / 2.0 - zj0
            for u0, u1 in self.plateEndFingers(stand)[1]:
                self.rectangularHole(t + (u0 + u1) / 2.0, zc, u1 - u0, t)
        self.move(tw, th, move)

    # ------------------------------------------------------------------
    # Beschriftung: Maße als Text im ersten Seitenteil (Option "labels" von boxes.py)
    def beginPart(self, tw, th, move):
        return self.move(tw, th, move, True)

    def dimensionLines(self):
        t = self.thickness
        l0, l1 = self.endLengths()
        T = self.laenge - l0 - l1
        starts = self.notchLayout(l0, l1)
        n = len(starts)
        if n:
            front = starts[0] - l0
            back = (l0 + T) - (starts[-1] + self.notch_width)
            notch_line = "Einkerbungen %d | Rand vorn %.1f | hinten %.1f" % (
                n,
                front,
                back,
            )
            if self.notch_continuous:
                notch_line = (
                    "Vertiefung durchgehend, Breite %.1f | Rand vorn %.1f | hinten %.1f"
                    % (
                        starts[-1] + self.notch_width - starts[0],
                        front,
                        back,
                    )
                )
        else:
            notch_line = "Einkerbungen 0"
        if self.ends == "hook":
            end_line = "Haken %.1f x %.1f | Luecke %.1f | Rahmenkoerper %.1f" % (
                self.hook_width,
                self.hook_height,
                self.hook_gap,
                T,
            )
        else:
            end_line = "Ohr %.1f | Rahmenkoerper %.1f" % (self.hang_inset, T)
        plates = self.braceEnds()
        if plates:
            end_line += " | Platte %.1f x %.1f" % (self.breite + 2 * t, plates[0][0])
        lines = [
            "Breite %.1f | Innen %.1f | Materialdicke %.1f"
            % (self.breite + 2 * t, self.breite, t),
            end_line,
            notch_line,
        ]
        if self.stands:
            lines.append(
                "Rahmenhoehe %.1f | Gesamthoehe %.1f (mit Staendern)"
                % (self.hoehe, self.hoehe + self.stand_height)
            )
        else:
            lines.append("Rahmenhoehe %.1f" % self.hoehe)
        return lines

    def writeLabels(self):
        """Schreibt die Maße zeilenweise in den Rahmenkörper der ersten Seitenwand, unterhalb
        der Einkerbungen. Schriftgröße und Zeilenabstand werden so gewählt, dass der Text in
        die freie Fläche passt: Höhe von der Unterkante des Rahmens bis unter die
        Einkerbungen, Breite zwischen den beiden Enden (Innenseiten von Stirn-/Rückwand)."""
        l0, l1 = self.endLengths()
        sh = self.stand_height if self.stands else 0.0
        margin = 3.0
        lines = self.dimensionLines()
        n = len(lines)
        if not n:
            return
        d = self.notch_depth if self.notchLayout(l0, l1) else 0.0
        avail_h = self.hoehe - d - 2 * margin  # Höhe der freien Fläche
        avail_w = (self.laenge - l0 - l1) - 2 * margin - 2.0  # Breite der freien Fläche
        if avail_h <= 0 or avail_w <= 0:
            return
        maxlen = max(len(line) for line in lines)
        # Zeilenabstand = 1.4 x Schriftgröße; Breite eines Zeichens ca. 0.6 x Schriftgröße
        fs = min(6.0, avail_h / (1.0 + 1.4 * (n - 1)), avail_w / (0.6 * maxlen))
        if fs < 1.5:  # zu klein zum Lesen
            return
        lh = 1.4 * fs
        x0 = l0 + margin + 1.0
        z0 = sh + self.hoehe - d - margin - fs  # Grundlinie der ersten Zeile
        for k, line in enumerate(lines):
            try:
                self.text(
                    line,
                    x0,
                    z0 - lh * k,
                    fontsize=fs,
                    align="left",
                    color=ANNOTATION_COLOR,
                )
            except TypeError:
                self.text(line, x0, z0 - lh * k)

    # ------------------------------------------------------------------
    def render(self):
        self.checkParams()
        # Layout: die beiden langen Seitenwände übereinander (Breite = y), darüber die
        # kleinen Teile (Stirn-/Rückwand, Platten, Verstrebungen am Ständer) in einer Reihe
        # nebeneinander. So bleibt die Gesamtbreite bei etwa y.
        self.sideWall(move="up", info=True)
        self.sideWall(move="up")
        stand0, stand1 = self.standSides()
        kind0, kind1 = self.endKinds()
        self.endWall(move="right", stand=stand0, kind=kind0)
        self.endWall(move="right", stand=stand1, kind=kind1)
        for length, stand in self.braceEnds():
            self.earPlate(length, stand, move="right")
        n = sum(self.standSides()) if self.stands and self.stand_brace else 0
        if n:
            self.braceStack(n, move="right")
