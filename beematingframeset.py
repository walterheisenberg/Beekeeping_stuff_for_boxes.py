#!/usr/bin/env python3
# Copyright (C) 2013-2026
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import math

from boxes import Boxes, Color


class BeeMatingFrameSet(Boxes):
    """Rähmchen für Begattungskästchen, platzsparend angeordnet

    Variante 1 (Klick): T-Ausschnitt in der Oberseite, einklickbare Seitenteile.
    Variante 2 (ApideaStyle): Wie beim Apidea Kunststoff-Rähmchen, zusätzlich mit
    Nut für die Mittelwand im Oberträger
    Variante 3 (Klick2): Oberträger mit Einkerbungen, der durch die T-förmigen
    Querschlitze der Seitenteile gesteckt wird; Mittelwand in einem Längsschlitz.
    """

    variant: str
    width: float
    length: float
    ear_length: float
    height: float
    notches: int
    count: int
    layout_width: float
    top_distance: float
    corner_radius: float

    description = """Rähmchen für Begattungskästchen (je ein Oberträger und zwei Seitenteile)
    Variante 1 (Klick): T-Ausschnitt in der Oberseite, einklickbare Seitenteile.
    Variante 2 (ApideaStyle): Wie beim Apidea Kunststoff-Rähmchen, zusätzlich mit
    Nut für die Mittelwand im Oberträger.
    Variante 3 (Klick2): Oberträger mit Einkerbungen, der durch die T-förmigen
    Querschlitze der Seitenteile gesteckt wird; Mittelwand in einem Längsschlitz."""

    ui_group = "Beekeeping"

    # Varianten (Auswahl --variant)
    KLICK = "Klick"  # Variante 1
    APIDEA_STYLE = "ApideaStyle"  # Variante 2
    KLICK2 = "Klick2"  # Variante 3
    ALL = "Alle"  # Variante 4: je ein Rähmchen aller drei Varianten

    # Apidea-Standardwerte der einstellbaren Felder (Default und Hilfetext)
    APIDEA = {
        "width": 25.0,  # Gesamtbreite des Oberträgers
        "length": 118.0,  # Gesamtlänge des Oberträgers
        "ear_length": 6.0,  # Ohrenlänge: von außen bis zum Anfang des Seitenteils
        "height": 106.0,  # Höhe der Seitenteile
        "notches": 2,  # Anzahl der Rundungen am Rand
    }

    # Feste Maße in mm (Apidea, aus Zeichnung + Maßstabsbild) - nicht einstellbar
    MIN_WALL = 2.0  # kleinste erlaubte Reststärke zwischen Ausschnitt und Rand
    MIN_TOP_DISTANCE = (
        2.0  # kleinster oberer Abstand zum Oberträger (Rundungen am Kopf)
    )
    SIDE_MIN_EXTRA = 10.0  # Mindestlänge unter Schlitzspitze bzw. Verjüngung

    # Variante 3 (Klick2): Der dünne Schnitt im Seitenteil beginnt um dieses
    # Vielfache von burn (Schnittfuge/2) vor dem Ende des breiten Schlitzes,
    # damit zwischen beiden keine Brücke stehen bleibt.
    SLIT_OVERLAP_BURN = 3

    # Gemeinsame maximale Breite (breiteste Stelle) für ApideaStyle und Klick2
    SIDE_MAX_WIDTH = 35.0

    # Alle Varianten (nicht einstellbar)
    SLIT_WIDTH = 2.0  # Breite der Nut bzw. des Schlitzes für die Mittelwand
    HEAD_LENGTH = (
        30.0  # Länge des breiten Kopfteils der Seitenteile (ApideaStyle, Klick2)
    )
    HEAD_NOTCH_DEPTH = (
        2.0  # Tiefe der Einschnitte an den äußeren Längskanten des Kopfteils
    )
    HEAD_NOTCH_LENGTH = 14.0  # Länge der Einschnitte; sie liegen mittig im Kopfteil
    # Klick2: Maße ergeben sich aus der Breite des Oberträgers bzw. der Höhe des Seitenteils
    CUT_DEPTH_RATIO = 0.06  # Tiefe der Einkerbungen = Anteil der Oberträgerbreite
    SLIT_WIDE_RATIO = (
        0.33  # Länge des breiten Längsschlitzes = Anteil der Seitenteilhöhe
    )
    SLIT_THIN_RATIO = (
        0.283  # Länge des dünnen Schnitts darunter = Anteil der Seitenteilhöhe
    )
    # ApideaStyle und Klick2 (nicht einstellbar)
    TAPER_LENGTH = 10.0  # Länge des Übergangs vom breiten zum schmalen Seitenteil
    # Schräge der Einschnitte an den Längskanten: Länge in Längsrichtung je mm Tiefe
    SIDE_NOTCH_SLOPE = 1.25 / 1.5

    # Rundungen am Rand (alle Varianten gleich)
    NOTCH_RADIUS = 10.0
    NOTCH_DEPTH = 7.5  # Tiefe vom Rand
    NOTCH_CENTER = 29.5  # Mitte vom Ende (bei 2)

    # Maße (Labels) auf Oberträger und Seitenteilen
    TAB_MIN_LENGTH = (
        10  # Kanten ab dem 10-fachen der Stegbreite (tabs) bekommen einen Steg
    )

    LABEL_SIZE = 3.0  # Start-Schriftgröße der Maße in mm
    LABEL_MARGIN = 0.8  # Mindestabstand zu Kanten und Schnitten in mm
    LABEL_MIN_SIZE = 1.5  # kleinste Schriftgröße der Maße in mm
    LABEL_CHAR_WIDTH = 0.65  # Zeichenbreite relativ zur Schriftgröße (Schätzung)
    LABEL_STEP = 0.5  # Raster bei der Suche nach einem freien Platz in mm

    # Anordnung mehrerer Rähmchen
    NEST_MARGIN = 0.5
    PROFILE_STEP = 0.25  # Schrittweite beim Abtasten der Seitenteil-Kontur in mm
    MAX_COUNT = 20  # größte erlaubte Anzahl Rähmchen
    MAX_ASPECT = 2.0  # größtes Seitenverhältnis der automatischen Anordnung

    # Einheitlicher Radius für Kopfbereich, Einkerbungen und Schultern
    CAP_RADIUS = 0.75

    # Seitenteil (Klick / Standard) Maße in mm bzw. Grad
    # Abstände je Seite zur Oberträgerkante: Breite = Oberträgerbreite - 2 * Abstand
    SIDE_HEAD_INSET = 1.85  # Kopf
    SIDE_NECK_INSET = (
        4.7  # Hals unter dem Kopf (= Breite des T-Schlitzes im Oberträger)
    )
    SIDE_TAPER_ANGLE = (
        2.5  # Verjüngung der Seitenkanten von der Schulter bis unten (je Seite)
    )
    # Schlitz: Breite oben und Tiefe ergeben sich aus den Maßen des Seitenteils
    SIDE_SLIT_WIDTH_RATIO = 0.183  # Schlitzbreite oben = Anteil der Seitenteilbreite
    SIDE_SLIT_DEPTH_RATIO = (
        0.444  # Tiefe des Schlitzendes ab Oberkante = Anteil der Höhe
    )
    SIDE_SLIT_TAPER_ANGLE = 0.75  # Verengung des Schlitzes nach unten (je Seite)

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.argparser.set_defaults(labels=False)  # Maße standardmäßig aus
        if not any(
            "--thickness" in action.option_strings for action in self.argparser._actions
        ):
            self.argparser.add_argument(
                "--thickness",
                action="store",
                type=float,
                default=3.0,
                help="Materialstärke in mm (Variante 2: Höhe der Aussparungen)",
            )
        self.argparser.add_argument(
            "--variant",
            action="store",
            type=str,
            default=self.KLICK,
            choices=[self.KLICK, self.APIDEA_STYLE, self.KLICK2, self.ALL],
            help="Variante 1 = Klick; Variante 2 = ApideaStyle; Variante 3 = Klick2; "
            "Variante 4 = Alle (je ein Rähmchen aller drei Varianten)",
        )
        self.argparser.add_argument(
            "--width",
            action="store",
            type=float,
            default=self.APIDEA["width"],
            help=f"Gesamtbreite des Oberträgers in mm (Apidea: {self.APIDEA['width']:g})",
        )
        self.argparser.add_argument(
            "--length",
            action="store",
            type=float,
            default=self.APIDEA["length"],
            help=f"Gesamtlänge des Oberträgers in mm (Apidea: {self.APIDEA['length']:g})",
        )
        self.argparser.add_argument(
            "--ear_length",
            action="store",
            type=float,
            default=self.APIDEA["ear_length"],
            help="Ohrenlänge in mm",
        )
        self.argparser.add_argument(
            "--height",
            action="store",
            type=float,
            default=self.APIDEA["height"],
            help=f"Höhe der Seitenteile in mm (Apidea: {self.APIDEA['height']:g})",
        )
        self.argparser.add_argument(
            "--notches",
            action="store",
            type=int,
            default=self.APIDEA["notches"],
            choices=[0, 1, 2],
            help="Anzahl der runden Aussparungen für Zellen am Rand des Oberträgers",
        )
        self.argparser.add_argument(
            "--corner_radius",
            action="store",
            type=float,
            default=1.0,
            help="Rundung der Außenecken und des unteren Seitenteil-Endes",
        )
        self.argparser.add_argument(
            "--top_distance",
            action="store",
            type=float,
            default=4.0,
            help="Oberer Abstand zum Oberträger in mm",
        )
        # Standard-boxes.py hat weder settingsGroup noch addSettingsArgs
        self.argparser.add_argument(
            "--count",
            action="store",
            type=int,
            default=1,
            help="Anzahl der Rähmchen (bei Variante 4 immer eines je Variante)",
        )
        self.argparser.add_argument(
            "--layout_width",
            action="store",
            type=float,
            default=0.0,
            help="Maximale Breite der Anordnung in mm",
        )

    # ------------------------------------------------------------------
    # Hilfsfunktionen
    # ------------------------------------------------------------------
    def notch_geometry(self):
        r = self.NOTCH_RADIUS
        c = r - self.NOTCH_DEPTH
        h = math.sqrt(r * r - c * c)
        a = math.degrees(math.asin(h / r))
        return c, h, a

    def notch_centers(self, l):
        if self.notches == 0:
            return []
        if self.notches == 1:
            return [l / 2]
        return [self.NOTCH_CENTER, l - self.NOTCH_CENTER]

    @staticmethod
    def rect_distance(px, py, x0, y0, x1, y1):
        dx = max(x0 - px, 0, px - x1)
        dy = max(y0 - py, 0, py - y1)
        return math.hypot(dx, dy)

    def check_dimensions(self, w, l, e) -> None:
        wall = self.MIN_WALL
        tw, th, sw = self.t_width(w), self.thickness, self.SLIT_WIDTH
        c, _, _ = self.notch_geometry()
        centers = self.notch_centers(l)

        self.check_ear(e, wall)
        if w < tw + 2 * wall:
            raise ValueError(
                f"Die Breite muss mindestens {tw + 2 * wall} mm betragen "
                "(T-Ausschnitt plus Rand)."
            )
        if l < 2 * (e + th) + wall:
            raise ValueError(
                "Länge zu klein: Länge muss größer als 2 x (Ohrenlänge + T-Höhe) sein."
            )
        self.check_notch_length(l, self.corner_radius)

        xl, xr = (w - tw) / 2, (w + tw) / 2
        sl, sr = (w - sw) / 2, (w + sw) / 2
        parts = [
            (xl, e, xr, e + th),
            (xl, l - e - th, xr, l - e),
            (sl, e + th, sr, l - e - th),
        ]
        for cy in centers:
            for x0, y0, x1, y1 in parts:
                dist = self.rect_distance(w + c, cy, x0, y0, x1, y1)
                if dist - self.NOTCH_RADIUS < wall:
                    raise ValueError(
                        "Der Ausschnitt kommt einer Rundung zu nah "
                        f"(Rest unter {wall} mm): Breite vergrößern oder "
                        "Ohrenlänge verkleinern."
                    )

    def t_width(self, w):
        return 2 * self.side_neck_half(w)

    def side_neck_end(self):
        return self.top_distance + self.thickness

    def side_head_half(self, w):
        return w / 2 - self.SIDE_HEAD_INSET

    def side_neck_half(self, w):
        return w / 2 - self.SIDE_NECK_INSET

    def side_edge_half(self, w, d):
        """Halbe Breite der Seitenkante in der Tiefe d unter der Oberkante (ab der Schulter)."""
        taper = math.tan(math.radians(self.SIDE_TAPER_ANGLE))
        return self.side_head_half(w) - (d - self.side_neck_end()) * taper

    def side_slit(self, w, h):
        """Schlitz des Seitenteils: (halbe Breite oben, halbe Breite der Endpunkte,
        Tiefe, Radius des runden Endes). Der Radius ist so gewählt, dass das runde Ende
        beide Seiten genau berührt (kein gerades Stück dazwischen)."""
        angle = math.radians(self.SIDE_SLIT_TAPER_ANGLE)
        top = self.SIDE_SLIT_WIDTH_RATIO * self.side_head_half(w)
        depth = self.SIDE_SLIT_DEPTH_RATIO * h
        end = top - depth * math.tan(angle)
        return top, end, depth, end / math.tan(math.pi / 4 - angle / 2)

    def side_bottom_width(self, w, h):
        if self.variant in (self.APIDEA_STYLE, self.KLICK2):
            return w
        return 2 * self.side_edge_half(w, h)

    def side_cell_width(self, w):
        if self.variant == self.KLICK:
            return 2 * self.side_head_half(w)
        return self.SIDE_MAX_WIDTH

    def check_side(self, w, h) -> None:
        min_h = self.SIDE_MIN_EXTRA / (
            1 - self.SIDE_SLIT_DEPTH_RATIO
        )  # Rand unter dem Schlitz
        if h < min_h:
            raise ValueError(
                f"Die Höhe muss mindestens {min_h:.1f} mm betragen "
                "(Länge des Schlitzes plus Rand)."
            )
        top, _, depth, radius = self.side_slit(w, h)
        if 2 * radius < self.SLIT_WIDTH:
            raise ValueError(
                f"Der Schlitz würde am Ende schmaler als {self.SLIT_WIDTH} mm: "
                "Breite vergrößern oder Höhe verkleinern."
            )
        if depth - 2 * radius < self.side_neck_end():
            raise ValueError(
                "Das Seitenteil ist zu kurz: der Schlitz muss unter dem Hals enden."
            )
        taper = math.tan(math.radians(self.SIDE_SLIT_TAPER_ANGLE))
        wall_end = (self.side_edge_half(w, depth - radius) - radius) * math.cos(
            math.radians(self.SIDE_TAPER_ANGLE)
        )
        wall_neck = self.side_neck_half(w) - (top - self.top_distance * taper)
        if min(wall_end, wall_neck) < self.MIN_WALL:
            raise ValueError(
                "Seitenteil zu schmal: neben dem Schlitz bleibt weniger als "
                f"{self.MIN_WALL} mm Material. Breite vergrößern."
            )

    # ------------------------------------------------------------------
    # Zeichnen
    # ------------------------------------------------------------------
    def slot(self, w, l, e) -> None:
        tw, th, sw = self.t_width(w), self.thickness, self.SLIT_WIDTH
        side = (tw - sw) / 2
        stem = l - 2 * e - 2 * th

        self.ctx.save()
        self.set_source_color(Color.INNER_CUT)
        self.moveTo((w - tw) / 2, e, 90)
        for length, angle in (
            (th, -90),
            (side, 90),
            (stem, 90),
            (side, -90),
            (th, -90),
            (tw, -90),
            (th, -90),
            (side, 90),
            (stem, 90),
            (side, -90),
            (th, -90),
            (tw, -90),
        ):
            self.edge(length)
            self.corner(angle)
        self.ctx.stroke()
        self.ctx.restore()

    def notch(self) -> None:
        _, _, a = self.notch_geometry()
        self.corner(a)
        self.corner(-2 * a, self.NOTCH_RADIUS)
        self.corner(a)

    def notch_events(self, l):
        """Runde Aussparungen am Rand als (Anfang, Ende, Art) entlang der Länge."""
        _, h, _ = self.notch_geometry()
        return [(cy - h, cy + h, "arc") for cy in self.notch_centers(l)]

    def tab_count(self, length) -> int:
        """Anzahl der Haltestege einer freien Außenkante: einer, wenn die Einstellung tabs
        gesetzt und die Kante lang genug ist (kürzere würden ganz wegfallen)."""
        tabs = getattr(self, "tabs", 0)
        return 1 if tabs and length >= self.TAB_MIN_LENGTH * tabs else 0

    def long_edge(self, length) -> None:
        """Gerade Außenkante, bei Bedarf mit Haltesteg."""
        self.edge(length, tabs=self.tab_count(length))

    def outline_bar(self, l, bar_end, left_side, events, cut_depth=0.0) -> None:
        """Gemeinsame Kontur des Oberträgers aller Varianten. bar_end zeichnet eine
        Schmalseite (ohne die abschließende Ecke), left_side die linke Längsseite
        (ohne die abschließende Ecke), events die Aussparungen der rechten Längsseite."""
        r = self.corner_radius
        self.moveTo(r, 0)
        bar_end()
        self.corner(90, r)
        pos = r
        for y0, y1, kind in events:
            self.long_edge(y0 - pos)
            if kind == "cut":
                self.cutout(cut_depth, self.thickness)
            else:
                self.notch()
            pos = y1
        self.long_edge(l - r - pos)
        self.corner(90, r)
        bar_end()
        self.corner(90, r)
        left_side()
        self.corner(90, r)

    def outline(self, w, l) -> None:
        r = self.corner_radius
        self.outline_bar(
            l,
            lambda: self.edge(w - 2 * r),
            lambda: self.long_edge(l - 2 * r),
            self.notch_events(l),
        )

    def rounded_polygon(self, vertices, tab_edges=()) -> None:
        n = len(vertices)

        def turn(i):
            ax, ay, _ = vertices[i - 1]
            bx, by, _ = vertices[i]
            cx, cy, _ = vertices[(i + 1) % n]
            abx, aby, bcx, bcy = bx - ax, by - ay, cx - bx, cy - by
            return math.degrees(
                math.atan2(abx * bcy - aby * bcx, abx * bcx + aby * bcy)
            )

        angles = [turn(i) for i in range(n)]
        tans = [
            vertices[i][2] * math.tan(math.radians(abs(angles[i])) / 2)
            for i in range(n)
        ]

        x0, y0, _ = vertices[0]
        x1, y1, _ = vertices[1]
        heading = math.atan2(y1 - y0, x1 - x0)
        self.moveTo(
            x0 + tans[0] * math.cos(heading),
            y0 + tans[0] * math.sin(heading),
            math.degrees(heading),
        )
        for i in range(n):
            j = (i + 1) % n
            length = math.hypot(
                vertices[j][0] - vertices[i][0], vertices[j][1] - vertices[i][1]
            )
            straight = max(length - tans[i] - tans[j], 0)
            self.edge(straight, tabs=self.tab_count(straight) if i in tab_edges else 0)
            self.corner(angles[j], vertices[j][2])

    def side_vertices(self, w, h):
        hc = self.side_head_half(w)
        hn = self.side_neck_half(w)
        hb = self.side_edge_half(w, h)
        top, end, depth, radius = self.side_slit(w, h)
        cr = self.corner_radius

        def v(x, d, r=0.0):
            return (hc + x, h - d, r)

        return [
            v(-hb, h, cr),  # 1. Unteres Ende links
            v(hb, h, cr),  # 2. Unteres Ende rechts
            v(
                hc, self.side_neck_end(), self.CAP_RADIUS
            ),  # 3. Unteres, äußeres Ende der Einkerbung (rechts)
            v(
                hn, self.side_neck_end(), self.CAP_RADIUS
            ),  # 4. Unteres, inneres Ende der Einkerbung (rechts)
            v(
                hn, self.top_distance, self.CAP_RADIUS
            ),  # 5. Oberes, inneres Ende der Einkerbung (rechts)
            v(
                hc, self.top_distance, self.CAP_RADIUS
            ),  # 6. Oberes, äußeres Ende der Einkerbung (rechts)
            v(hc, 0, self.CAP_RADIUS),  # 7. Oberes Ende / Spitze rechts
            v(top, 0),
            v(end, depth, radius),
            v(-end, depth, radius),
            v(-top, 0),
            v(-hc, 0, self.CAP_RADIUS),  # 7. Oberes Ende / Spitze links
            v(
                -hc, self.top_distance, self.CAP_RADIUS
            ),  # 6. Oberes, äußeres Ende der Einkerbung (links)
            v(
                -hn, self.top_distance, self.CAP_RADIUS
            ),  # 5. Oberes, inneres Ende der Einkerbung (links)
            v(
                -hn, self.side_neck_end(), self.CAP_RADIUS
            ),  # 4. Unteres, inneres Ende der Einkerbung (links)
            v(
                -hc, self.side_neck_end(), self.CAP_RADIUS
            ),  # 3. Unteres, äußeres Ende der Einkerbung (links)
        ]

    # ------------------------------------------------------------------
    # Gemeinsame Hilfsfunktion für ApideaStyle und Klick2 (Unterer Teil)
    # ------------------------------------------------------------------
    def side_profile_lower(self, h, narrow, wide, wide_end, notch_ref, wide_radius=0.0):
        prof = [(narrow, h, self.corner_radius)]
        if wide - narrow > 1e-9:
            prof += [
                (narrow, wide_end + self.TAPER_LENGTH, 0.0),
                (wide, wide_end, wide_radius),
            ]
        nd = self.HEAD_NOTCH_DEPTH
        # mittig zwischen dem Ende des Querschlitzes (notch_ref) und dem Ende des Kopfteils
        top = (notch_ref + wide_end - self.HEAD_NOTCH_LENGTH) / 2
        bottom = top + self.HEAD_NOTCH_LENGTH
        slope = nd * self.SIDE_NOTCH_SLOPE
        prof += [
            (wide, bottom, 0.0),
            (wide - nd, bottom - slope, 0.0),
            (wide - nd, top + slope, 0.0),
            (wide, top, 0.0),
        ]
        return prof

    @staticmethod
    def mirror_profile(half, cx, h, mid=()):
        right = [(cx + hw, h - d, r) for hw, d, r in half]
        left = [(cx - hw, h - d, r) for hw, d, r in reversed(half)]
        verts = right + list(mid) + left
        return verts[-1:] + verts[:-1]

    def check_side_notch(self, ref, min_offset, end_depth, wide, inner_min) -> None:
        """Einschnitte im Kopfteil: mittig zwischen dem Ende des Querschlitzes (ref) und
        dem Ende des Kopfteils (end_depth)."""
        nd, nl = self.HEAD_NOTCH_DEPTH, self.HEAD_NOTCH_LENGTH
        if (end_depth - ref - nl) / 2 < min_offset:
            raise ValueError(
                "Zwischen Querschlitz und Ende des Kopfteils ist zu wenig Platz für die "
                "Einschnitte: oberer Abstand plus Materialstärke höchstens "
                f"{end_depth - nl - 2 * min_offset:g} mm."
            )
        if wide - nd < inner_min:
            raise ValueError("Die Einschnitte sind zu tief.")

    def check_ear(self, e, minimum) -> None:
        if e < minimum:
            raise ValueError(f"Die Ohrenlänge muss mindestens {minimum} mm betragen.")

    def check_notch_length(self, l, *margins) -> None:
        """Mindestlänge des Oberträgers für die runden Aussparungen. Bei einer einzelnen
        Rundung (Mitte) kommen zur halben Rundungsbreite noch die margins hinzu."""
        _, h, _ = self.notch_geometry()
        if self.notches == 2:
            min_len = 2 * (self.NOTCH_CENTER + h)
        elif self.notches == 1:
            reach = h
            for m in margins:
                reach += m
            min_len = 2 * reach
        else:
            min_len = 0.0
        if l < min_len:
            raise ValueError(
                f"Die Länge muss mindestens {min_len:.1f} mm betragen, "
                "damit die Rundung(en) Platz haben."
            )

    def check_notch_slit(self, w, target) -> None:
        if self.notches and self.NOTCH_DEPTH >= (w - self.SLIT_WIDTH) / 2:
            raise ValueError(f"Die Rundung reicht bis in {target}.")

    # ------------------------------------------------------------------
    # Variante 2: Apidea-Style
    # ------------------------------------------------------------------
    def a_tab_width(self, w):
        """Jede Nase am Oberträger = exakt 0.24 * w"""
        return w * 0.24

    def a_tongue_width(self, w):
        """Steg am Seitenteil und Aussparung im Oberträger = exakt 0.52 * w"""
        return w * 0.52

    def check_apidea(self, w, l, e, h) -> None:
        t = self.a_tab_width(w)
        r = self.corner_radius
        _, nh, _ = self.notch_geometry()
        mat = self.thickness
        depth = e + mat
        min_tongue = 2 * self.MIN_WALL
        if self.a_tongue_width(w) < min_tongue:
            min_w = w + (min_tongue - self.a_tongue_width(w))
            raise ValueError(
                "Die Zunge des Seitenteils würde schmaler als "
                f"{min_tongue} mm (Breite zu klein). "
                f"Mindestens {min_w:.1f} mm Breite erforderlich."
            )
        self.check_ear(e, 2 * r)
        if 2 * r > t:
            raise ValueError(
                f"Die Rundung der Außenecken darf höchstens {t / 2:g} mm betragen "
                "(Breite der Nasen)."
            )
        if self.notches == 2 and depth > self.NOTCH_CENTER - nh - self.MIN_WALL:
            raise ValueError(
                "Die Ohrenlänge oder Materialstärke ist zu groß: die "
                "Aussparung kommt der Rundung zu nah."
            )
        self.check_notch_length(l, depth, self.MIN_WALL)
        self.check_side_notch(
            self.top_distance + mat,
            self.CAP_RADIUS,
            self.HEAD_LENGTH,
            self.SIDE_MAX_WIDTH / 2,
            w / 2,
        )
        if l - 2 * (depth + self.MIN_WALL) <= 0:
            raise ValueError("Der Oberträger ist zu kurz für die Nut der Mittelwand.")
        self.check_notch_slit(w, "die Nut der Mittelwand")
        top = self.HEAD_LENGTH + self.TAPER_LENGTH
        if h < top + self.SIDE_MIN_EXTRA:
            raise ValueError(
                f"Die Höhe muss mindestens {top + self.SIDE_MIN_EXTRA:.1f} mm betragen."
            )

    def outline_apidea(self, w, l, depth) -> None:
        r = self.corner_radius
        t = self.a_tab_width(w)  # Exakt 0.24 * w
        gap = self.a_tongue_width(w)  # Exakt 0.52 * w

        def bar_end():
            self.edge(t - 2 * r)
            self.corner(90, r)
            self.edge(depth - r)
            self.corner(-90)
            self.edge(gap)
            self.corner(-90)
            self.edge(depth - r)
            self.corner(90, r)
            self.edge(t - 2 * r)

        self.outline_bar(
            l, bar_end, lambda: self.long_edge(l - 2 * r), self.notch_events(l)
        )

    def side_vertices_apidea(self, w, h):
        d_cap = self.top_distance
        d_shoulder = d_cap + self.thickness
        tongue_half = self.a_tongue_width(w) / 2
        wide = self.SIDE_MAX_WIDTH / 2
        narrow = w / 2
        half = self.side_profile_lower(
            h, narrow, wide, self.HEAD_LENGTH, d_shoulder, self.CAP_RADIUS
        )
        half += [
            (wide, d_shoulder, self.CAP_RADIUS),
            (tongue_half, d_shoulder, 0.0),
            (tongue_half, d_cap, 0.0),
            (wide, d_cap, self.CAP_RADIUS),
            (wide, 0.0, self.CAP_RADIUS),
        ]
        return self.mirror_profile(half, wide, h)

    # ------------------------------------------------------------------
    # Variante 3: Klick2
    # ------------------------------------------------------------------
    def check_klick2(self, w, l, e, h) -> None:
        t = self.thickness
        d = self.klick2_cut_depth(w)
        head = self.SIDE_MAX_WIDTH
        if w > head:
            raise ValueError(
                f"Die Breite darf bei Klick2 höchstens {head:g} mm betragen "
                "(Breite der Seitenteile)."
            )
        if self.SLIT_WIDTH >= w - 2 * d:
            raise ValueError("Der Mittelwand-Schlitz ist zu breit.")
        self.check_ear(e, 2 * self.corner_radius)
        min_h = (self.top_distance + t) / self.SLIT_WIDE_RATIO
        if h < min_h:
            raise ValueError(
                "Der breite Längsschlitz muss mindestens bis hinter den Querschlitz "
                f"reichen: Höhe mindestens {min_h:.1f} mm."
            )
        if self.HEAD_LENGTH + self.TAPER_LENGTH > h:
            raise ValueError("Kopf und Übergang sind länger als das Seitenteil.")
        self.check_side_notch(
            self.top_distance + t,
            0.0,
            self.HEAD_LENGTH,
            head / 2,
            self.SLIT_WIDTH / 2 + self.MIN_WALL,
        )
        if l < 2 * (e + t) + 1:
            raise ValueError("Der Oberträger ist zu kurz.")
        self.check_notch_slit(w, "den Mittelwand-Schlitz")
        self.klick2_events(l, e)

    def klick2_cut_depth(self, w):
        return self.CUT_DEPTH_RATIO * w

    def klick2_slit_wide(self, h):
        return self.SLIT_WIDE_RATIO * h

    def klick2_slit_thin(self, h):
        return self.SLIT_THIN_RATIO * h

    def klick2_events(self, l, e):
        t = self.thickness
        events = [(e, e + t, "cut"), (l - e - t, l - e, "cut")]
        events += self.notch_events(l)
        events.sort()
        for (_, a1, _), (b0, _, _) in zip(events, events[1:]):
            if b0 < a1:
                raise ValueError(
                    "Rundungen und Einkerbungen überlappen sich: "
                    "Länge oder Ohrenlänge anpassen."
                )
        if events[0][0] < 0 or events[-1][1] > l:
            raise ValueError("Die Rundungen liegen außerhalb des Oberträgers.")
        return events

    def cutout(self, d, t) -> None:
        self.polyline(0, 90, d, -90, t, -90, d, 90)

    def slot_wall(self, w, l, margin) -> None:
        self.ctx.save()
        self.rectangularHole(w / 2, l / 2, self.SLIT_WIDTH, l - 2 * margin)
        self.ctx.restore()

    def outline_klick2(self, w, l, e) -> None:
        t, r = self.thickness, self.corner_radius
        d = self.klick2_cut_depth(w)
        events = self.klick2_events(l, e)

        def left_side():
            self.edge(e - r)
            self.cutout(d, t)
            self.long_edge(l - 2 * e - 2 * t)
            self.cutout(d, t)
            self.edge(e - r)

        self.outline_bar(l, lambda: self.edge(w - 2 * r), left_side, events, d)

    def side_vertices_klick2(self, w, h):
        bw = w / 2
        hc = self.SIDE_MAX_WIDTH / 2
        sw2 = self.SLIT_WIDTH / 2
        a = self.top_distance
        ct = self.thickness  # Höhe des Querschlitzes
        cl2 = (w - 2 * self.klick2_cut_depth(w)) / 2  # halbe Länge des Querschlitzes
        swl = self.klick2_slit_wide(h)

        half = self.side_profile_lower(
            h, bw, hc, self.HEAD_LENGTH, a + ct, self.CAP_RADIUS
        )
        half.append((hc, 0.0, self.CAP_RADIUS))

        def v(u, d):
            return (hc + u, h - d, 0.0)

        mid = [
            v(sw2, 0),
            v(sw2, a),
            v(cl2, a),
            v(cl2, a + ct),
            v(sw2, a + ct),
            v(sw2, swl),
            v(-sw2, swl),
            v(-sw2, a + ct),
            v(-cl2, a + ct),
            v(-cl2, a),
            v(-sw2, a),
            v(-sw2, 0),
        ]
        return self.mirror_profile(half, hc, h, mid)

    def draw_slit_klick2(self, w, h) -> None:
        overlap = self.SLIT_OVERLAP_BURN * self.burn
        x = self.SIDE_MAX_WIDTH / 2
        y = h - (self.klick2_slit_wide(h) - overlap) + self.burn
        self.ctx.save()
        self.set_source_color(Color.INNER_CUT)
        self.moveTo(x, y, -90)
        self.edge(self.klick2_slit_thin(h) + overlap)
        self.ctx.stroke()
        self.ctx.restore()

    # ------------------------------------------------------------------
    # Maße (Labels)
    # ------------------------------------------------------------------
    def label_size(self):
        return self.LABEL_SIZE

    def label_length(self, text, size):
        return len(text) * self.LABEL_CHAR_WIDTH * size

    def label_texts(self, dim):
        """Maß mit Materialstärke (d) und Burn (b); als Ausweichtext nur das Maß."""
        return [f"{dim:g} mm, d={self.thickness:g}, b={self.burn:g}", f"{dim:g} mm"]

    def layout_dimension_text(self, w, l, e):
        """Maß der Breite samt Materialstärke und Burn auf dem Oberträger (alle Varianten):
        Es steht längs im freien Streifen rechts neben der Mittelwand-Nut, mit Abstand zu
        Nut, Rand und runden Aussparungen. Liefert
        (x, y, Schriftgröße, Text, Drehwinkel) oder None, wenn kein Platz ist."""
        if not self.labels:
            return None
        m, step = self.LABEL_MARGIN, self.LABEL_STEP
        xa, xb = w / 2 + self.SLIT_WIDTH / 2 + m, w - m
        ya, yb = e + self.thickness + m, l - e - self.thickness - m
        c, _, _ = self.notch_geometry()
        centers = self.notch_centers(l)

        def fits(xc, yc, hx, hy):
            for cy in centers:
                dist = self.rect_distance(w + c, cy, xc - hx, yc - hy, xc + hx, yc + hy)
                if dist < self.NOTCH_RADIUS + m:
                    return False
            return True

        for text in self.label_texts(w):
            size = self.label_size()
            while size >= self.LABEL_MIN_SIZE - 1e-9:
                hx = size / 2
                hy = self.label_length(text, size) / 2
                offsets = [0.0]
                for k in range(1, int((xb - xa) / step) + 1):
                    offsets += [k * step, -k * step]
                for dx in offsets:  # von der Mitte des Streifens nach außen
                    xc = (xa + xb) / 2 + dx
                    if xc - hx < xa - 1e-9 or xc + hx > xb + 1e-9:
                        continue
                    runs, run = [], []
                    for j in range(max(int((yb - ya - 2 * hy) / step) + 1, 0)):
                        yc = ya + hy + j * step
                        if fits(xc, yc, hx, hy):
                            run.append(yc)
                        elif run:
                            runs.append(run)
                            run = []
                    if run:
                        runs.append(run)
                    if runs:
                        best = max(runs, key=len)  # längster freier Abschnitt
                        return xc, (best[0] + best[-1]) / 2, size, text, math.pi / 2
                size -= 0.25
        return None

    def draw_label(self, x, y, size, text, angle=0.0) -> None:
        """Maß in der Annotationsfarbe (wird nicht geschnitten), Mitte bei (x, y).
        angle in Bogenmaß."""
        self.text(
            text,
            x,
            y,
            math.degrees(angle),
            "middle center",
            size,
            Color.ANNOTATIONS,
        )

    def draw_dimension_text(self, layout) -> None:
        if not self.labels or not layout:
            return
        x, y, size, text, angle = layout
        self.draw_label(x, y, size, text, angle)

    @staticmethod
    def segment_hits_rect(p, q, x0, y0, x1, y1):
        dx, dy = q[0] - p[0], q[1] - p[1]
        t0, t1 = 0.0, 1.0
        for pk, qk in (
            (-dx, p[0] - x0),
            (dx, x1 - p[0]),
            (-dy, p[1] - y0),
            (dy, y1 - p[1]),
        ):
            if abs(pk) < 1e-12:
                if qk < 0:
                    return False
                continue
            r = qk / pk
            if pk < 0:
                if r > t1:
                    return False
                t0 = max(t0, r)
            else:
                if r < t0:
                    return False
                t1 = min(t1, r)
        return True

    @staticmethod
    def point_in_polygon(x, y, pts):
        inside = False
        n = len(pts)
        for i in range(n):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % n]
            if (y0 > y) != (y1 > y) and x < x0 + (y - y0) / (y1 - y0) * (x1 - x0):
                inside = not inside
        return inside

    def layout_plate_dimension_text(self, w, h):
        """Maß (Höhe) im Seitenteil, parallel zur langen Seite. Der Platz wird
        automatisch gesucht: möglichst mittig, mit Abstand zu allen Kanten,
        Schlitzen und Schnitten. Liefert (x, y, Schriftgröße, Text, Drehwinkel) oder None."""
        if not self.labels:
            return None
        verts = [(x, y) for x, y, _ in self.plate_vertices(w, h)]
        obstacles = []
        if self.variant == self.KLICK2:
            overlap = self.SLIT_OVERLAP_BURN * self.burn
            x = self.SIDE_MAX_WIDTH / 2
            y0 = h - (self.klick2_slit_wide(h) - overlap) + self.burn
            obstacles.append(((x, y0), (x, y0 - self.klick2_slit_thin(h) - overlap)))
        xs = [v[0] for v in verts]
        cx = (min(xs) + max(xs)) / 2
        half = (max(xs) - min(xs)) / 2
        m, step = self.LABEL_MARGIN, self.LABEL_STEP

        def fits(xc, yc, hx, hy):
            x0, x1, y0, y1 = xc - hx, xc + hx, yc - hy, yc + hy
            if not self.point_in_polygon(xc, yc, verts):
                return False
            n = len(verts)
            for i in range(n):
                if self.segment_hits_rect(verts[i], verts[(i + 1) % n], x0, y0, x1, y1):
                    return False
            for a, b in obstacles:
                if self.segment_hits_rect(a, b, x0, y0, x1, y1):
                    return False
            return True

        for text in self.label_texts(h):
            size = self.label_size()
            while size >= self.LABEL_MIN_SIZE - 1e-9:
                hx = size / 2 + m
                hy = self.label_length(text, size) / 2 + m
                offsets = [0.0]
                for k in range(1, int(half / step) + 1):
                    offsets += [k * step, -k * step]
                for dx in offsets:  # von der Mitte nach außen
                    xc = cx + dx
                    runs, run = [], []
                    n_y = int((h - 2 * hy) / step) + 1
                    for j in range(max(n_y, 0)):
                        yc = hy + j * step
                        if fits(xc, yc, hx, hy):
                            run.append(yc)
                        elif run:
                            runs.append(run)
                            run = []
                    if run:
                        runs.append(run)
                    if runs:
                        best = max(runs, key=len)  # längster freier Abschnitt
                        return xc, (best[0] + best[-1]) / 2, size, text, math.pi / 2
                size -= 0.25
        return None

    def draw_plate_dimension_text(self, layout) -> None:
        if not self.labels or not layout:
            return
        x, y, size, text, angle = layout
        self.draw_label(x, y, size, text, angle)

    # ------------------------------------------------------------------
    # Teile zeichnen (ohne Platzierung)
    # ------------------------------------------------------------------
    def plate_vertices(self, w, h):
        if self.variant == self.APIDEA_STYLE:
            return self.side_vertices_apidea(w, h)
        if self.variant == self.KLICK2:
            return self.side_vertices_klick2(w, h)
        return self.side_vertices(w, h)

    def draw_plate(self, w, h) -> None:
        if self.variant == self.KLICK2:
            self.draw_slit_klick2(w, h)
        # Maß zuerst zeichnen: rounded_polygon verändert das Koordinatensystem
        # (es bleibt am Startpunkt der Kontur gedreht stehen)
        self.draw_plate_dimension_text(self.plate_text_layout)
        vertices = self.plate_vertices(w, h)
        # Haltestege: untere Kante und die beiden langen Seitenkanten (Ecke 0 ist unten links)
        self.rounded_polygon(vertices, tab_edges=(0, 1, len(vertices) - 1))

    def draw_bar(self, w, l, e) -> None:
        self.draw_dimension_text(self.dimension_text_layout)
        if self.variant == self.APIDEA_STYLE:
            self.slot_wall(w, l, e + self.thickness + self.MIN_WALL)
            self.outline_apidea(w, l, e + self.thickness)
        elif self.variant == self.KLICK2:
            self.slot_wall(w, l, e)
            self.outline_klick2(w, l, e)
        else:
            self.slot(w, l, e)
            self.outline(w, l)

    def draw_item(self, kind, rotated, iw, ih, variant) -> None:
        if self.move(iw, ih, None, True):
            return
        self.variant = variant
        layouts = self.layouts[variant]
        self.dimension_text_layout, self.plate_text_layout = layouts
        with self.saved_context():
            if kind == "bar":
                self.draw_bar(self.width, self.length, self.ear_length)
            else:
                if rotated:
                    self.ctx.translate(iw, ih)
                    self.ctx.rotate(math.pi)
                self.draw_plate(self.width, self.height)
        self.move(iw, ih, None)

    def shift(self, dx, dy) -> None:
        if abs(dx) > 1e-9 or abs(dy) > 1e-9:
            self.ctx.translate(dx, dy)

    # ------------------------------------------------------------------
    # Anordnung mehrerer Rähmchen
    # ------------------------------------------------------------------
    @staticmethod
    def scan_half_width(vertices, cx, y):
        best = None
        n = len(vertices)
        for i in range(n):
            x0, y0, _ = vertices[i]
            x1, y1, _ = vertices[(i + 1) % n]
            if y < min(y0, y1) - 1e-9 or y > max(y0, y1) + 1e-9:
                continue
            if abs(y1 - y0) < 1e-9:
                xs = (x0, x1)
            else:
                xs = (x0 + (y - y0) / (y1 - y0) * (x1 - x0),)
            for x in xs:
                d = abs(x - cx)
                if best is None or d > best:
                    best = d
        return best

    def gap(self):
        # self.spacing (Standardeinstellung "spacing") enthält bereits 2 * burn
        return self.spacing

    def gap_rows(self):
        return self.spacing + 2 * self.burn

    def nests(self, va, vb):
        """Seitenteile derselben Variante sowie ApideaStyle und Klick2 passen ineinander."""
        return va == vb or {va, vb} == {self.APIDEA_STYLE, self.KLICK2}

    def nest_pitch(self, w, h, va, vb):
        """Abstand der Mitten zweier ineinander geschobener Seitenteile (a aufrecht,
        b um 180° gedreht)."""
        selected = self.variant
        self.variant = va
        verts_a, cell_a = self.plate_vertices(w, h), self.side_cell_width(w)
        self.variant = vb
        verts_b, cell_b = self.plate_vertices(w, h), self.side_cell_width(w)
        self.variant = selected
        cx_a = (min(v[0] for v in verts_a) + max(v[0] for v in verts_a)) / 2
        cx_b = (min(v[0] for v in verts_b) + max(v[0] for v in verts_b)) / 2
        ys = {0.0, float(h)}
        k = 1
        while k * self.PROFILE_STEP < h:
            ys.add(k * self.PROFILE_STEP)
            k += 1
        offset = 2 * self.burn
        for verts in (verts_a, verts_b):
            for _, vy, _ in verts:
                for yy in (vy, h - vy, h - vy + offset, h - vy - offset):
                    ys.add(min(max(yy, 0.0), float(h)))
        pitch = 0.0
        for y in ys:
            a = self.scan_half_width(verts_a, cx_a, y)
            if a is None:
                continue
            for dy in (-offset, 0.0, offset):
                yy = h - y + dy
                if 0.0 <= yy <= h:
                    b = self.scan_half_width(verts_b, cx_b, yy)
                    if b is not None:
                        pitch = max(pitch, a + b)
        margin = self.NEST_MARGIN if self.KLICK in (va, vb) else 0.0
        pitch += self.gap() + margin
        return min(pitch, (cell_a + cell_b) / 2 + self.gap())

    def pack_items(self, items, max_width, pitches):
        gap = self.gap()
        shelves = []
        cur = []
        for kind, iw, ih, variant in items:
            x, rot = 0.0, False
            if cur:
                pk, px, prot, pw, _, pv = cur[-1]
                if kind == "plate" and pk == "plate" and self.nests(pv, variant):
                    x, rot = px + (pw - iw) / 2 + pitches[(pv, variant)], not prot
                else:
                    x = px + pw + gap
                if x + iw > max_width + 1e-9:
                    shelves.append(cur)
                    cur = []
                    x, rot = 0.0, False
            cur.append((kind, x, rot, iw, ih, variant))
        if cur:
            shelves.append(cur)
        total_w = max(it[1] + it[3] for shelf in shelves for it in shelf)
        total_h = sum(max(it[4] for it in shelf) for shelf in shelves)
        total_h += self.gap_rows() * (len(shelves) - 1)
        return shelves, total_w, total_h

    def choose_layout(self, items, pitches):
        widest = max(iw for _, iw, _, _ in items)
        if self.layout_width > 0:
            if self.layout_width < widest:
                raise ValueError(
                    f"Die maximale Breite der Anordnung muss mindestens {widest:.1f} mm "
                    "betragen (breitestes Teil)."
                )
            return self.pack_items(items, self.layout_width, pitches)
        best, best_key = None, None
        fallback, fallback_key = None, None
        width = widest
        while True:
            result = self.pack_items(items, width, pitches)
            shelves, total_w, total_h = result
            area = total_w * total_h
            aspect = max(total_w, total_h) / min(total_w, total_h)
            if aspect <= self.MAX_ASPECT:
                key = (area, max(total_w, total_h))
                if best_key is None or key < best_key:
                    best, best_key = result, key
            key = (aspect, area)
            if fallback_key is None or key < fallback_key:
                fallback, fallback_key = result, key
            if len(shelves) == 1:
                break
            width += 1.0
        return best or fallback

    def render(self) -> None:
        w, l, e, h = self.width, self.length, self.ear_length, self.height
        selected = self.variant
        every = selected == self.ALL
        variants = [self.KLICK, self.APIDEA_STYLE, self.KLICK2] if every else [selected]
        count = 1 if every else self.count
        if not 1 <= count <= self.MAX_COUNT:
            raise ValueError(f"Die Anzahl muss zwischen 1 und {self.MAX_COUNT} liegen.")
        if self.spacing < 0:
            raise ValueError("Der Abstand zwischen den Teilen darf nicht negativ sein.")
        if self.corner_radius < 0:
            raise ValueError("Die Rundung der Außenecken darf nicht negativ sein.")
        if getattr(self, "tabs", 0) < 0:
            raise ValueError("Die Breite der Haltestege darf nicht negativ sein.")
        if 2 * self.corner_radius > min(w, l):
            raise ValueError(
                "Die Rundung der Außenecken ist zu groß für den Oberträger."
            )

        self.layouts = {}
        cells, pitches = {}, {}
        for v in variants:
            self.variant = v
            try:
                self.check_variant(w, l, e, h)
            except ValueError as error:
                if every:
                    raise ValueError(f"{v}: {error}") from None
                raise
            self.layouts[v] = (
                self.layout_dimension_text(w, l, e),
                self.layout_plate_dimension_text(w, h),
            )
            cells[v] = self.side_cell_width(w)
        for va in variants:
            for vb in variants:
                if self.nests(va, vb):
                    pitches[(va, vb)] = self.nest_pitch(w, h, va, vb)

        items = []
        for v in variants:
            items += [("bar", w, l, v)] * count + [("plate", cells[v], h, v)] * (
                2 * count
            )
        items.sort(key=lambda it: -it[2])
        shelves, _, _ = self.choose_layout(items, pitches)

        cur_x = 0.0
        for shelf in shelves:
            shelf_h = max(it[4] for it in shelf)
            for kind, x, rotated, iw, ih, variant in shelf:
                self.shift(x - cur_x, 0)
                cur_x = x
                self.draw_item(kind, rotated, iw, ih, variant)
            self.shift(-cur_x, shelf_h + self.gap_rows())
            cur_x = 0.0
        self.variant = selected

    def check_variant(self, w, l, e, h) -> None:
        if 2 * self.corner_radius > self.side_bottom_width(w, h):
            raise ValueError(
                "Die Rundung ist zu groß für die untere Kante der Seitenteile."
            )
        if self.top_distance < self.MIN_TOP_DISTANCE:
            raise ValueError(
                "Der obere Abstand zum Oberträger muss mindestens "
                f"{self.MIN_TOP_DISTANCE:g} mm betragen (Platz für die Abrundungen)."
            )
        if self.variant == self.APIDEA_STYLE:
            self.check_apidea(w, l, e, h)
        elif self.variant == self.KLICK2:
            self.check_klick2(w, l, e, h)
        else:
            self.check_dimensions(w, l, e)
            self.check_side(w, h)
