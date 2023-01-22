from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import*
from kivy.graphics import Color
from kivy.graphics import Rectangle

from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window

from CoolProp.CoolProp import PropsSI

Window.clearcolor = (0.5, 0.5, 0.5, 1)
Window.size = (600, 400)

class fPT_Screen(Screen):
    def __init__(self, name="fPT"):
        super(fPT_Screen, self).__init__(name=name)
        self.fPT = Button(text='f(PT)', background_color='yellow', on_release=self.tofPT)
        self.fPH = Button(text='f(PH)', background_color='green', on_release=self.tofPH)
        self.fP = Button(text='f(P)', background_color='blue', on_release=self.tofP)
        self.fT = Button(text='f(T)', background_color='red', on_release=self.tofT)
        self.name_fPT = Button(text='Свойства воды и пара. Фунцкия от Давления и Температуры.', background_color='yellow')
        self.label1 = Button(text='Давление, бар')
        self.label2 = Button(text='Температура, грЦ')
        self.hpt = Button(text='Энтальпия, кДж/кг')
        self.dpt = Button(text='Плотность, кг/м3')
        self.cpt = Button(text='Теплоёмкость(изобар), кДж/кг*K')
        self.lpt = Button(text='Коэф. теплопроводности, Вт/м*K')
        self.vpt = Button(text='Динамич. вязкость, Па*с')
        self.ppt = Button(text='Число Прандтля: ')
        self.phase = Button(text='Агрегатное состояние: ')
        self.author = Button(text='Автор - Денис Михалев.', color='black')
        self.input_dataP = TextInput(hint_text='Давление, бар', multiline=False, halign="center", input_filter='int')
        self.input_dataT = TextInput(hint_text='Температура, грЦ', multiline=False, halign="center", input_filter='int')
        self.input_dataP.bind(text=self.on_text)
        self.input_dataT.bind(text=self.on_text)

        flfPT = FloatLayout(size=(20, 20))
        al1 = AnchorLayout(anchor_y='bottom')
        al2 = AnchorLayout(anchor_y='top')
        bl1 = BoxLayout()
        bl2 = BoxLayout()
        gl1 = GridLayout(cols=2, rows=8, size_hint=(1, 0.8))
        gl2 = GridLayout(cols=1, rows=2, size_hint=(1, 0.2))

        gl1.add_widget(self.label1)
        gl1.add_widget(self.label2)
        gl1.add_widget(self.input_dataP)
        gl1.add_widget(self.input_dataT)
        gl1.add_widget(self.hpt)
        gl1.add_widget(self.dpt)
        gl1.add_widget(self.cpt)
        gl1.add_widget(self.lpt)
        gl1.add_widget(self.vpt)
        gl1.add_widget(self.ppt)
        gl1.add_widget(self.phase)
        gl1.add_widget(self.author)

        bl1.add_widget(self.fPT)
        bl1.add_widget(self.fPH)
        bl1.add_widget(self.fP)
        bl1.add_widget(self.fT)
        bl2.add_widget(self.name_fPT)

        gl2.add_widget(bl1)
        gl2.add_widget(bl2)

        al1.add_widget(gl1)
        al2.add_widget(gl2)
        flfPT.add_widget(al1)
        flfPT.add_widget(al2)

        self.add_widget(flfPT)


    def tofPT(self, fPT):
        self.manager.current = "fPT"

    def tofPH(self, fPH):
        self.manager.current = "fPH"

    def tofP(self, fP):
        self.manager.current = "fP"

    def tofT(self, fT):
        self.manager.current = "fT"

    def on_text(self, *args):
        A = 273.15
        B = 100000
        Pcrit = 221
        Pmin = 1
        Pmax = 500
        Tmin = 1
        Tmax = 700

        try:
            dataP = self.input_dataP.text
            if float(dataP) > Pmax:
                dataP = str(Pmax)
            else:
                dataP = self.input_dataP.text
        except:
            dataP = str(Pmin)

        try:
            dataT = self.input_dataT.text
            if float(dataT) > Tmax:
                dataT = str(Tmax)
            else:
                dataT = self.input_dataT.text
        except:
            dataT = str(Tmin)

        try:
            h = PropsSI('H', 'T', float(dataT) + A, 'P', float(dataP) * B, 'IF97::Water') / 1000
        except:
            h = 99999
        #print(dataP)
        try:
            if float(dataP) <= Pcrit:
            # hw = PropsSI('H','T',float(dataT)+A,'Q',0,'IF97::Water')
                hs = PropsSI('H', 'P', float(dataP)*B, 'Q', 1, 'IF97::Water') / 1000
            #print(hs)
            else:
                hs = 2800
        except:
            hs = 2800
        if dataP.isnumeric():
            if dataT.isnumeric():
                self.hpt.text = 'Энтальпия, кДж/кг: ' + str(round(h, 1))
                self.dpt.text = 'Плотность, кг/м3: ' + str(round(PropsSI('D', 'T', float(dataT)+A, 'P', float(dataP)*B, 'IF97::Water'), 3))
                self.cpt.text = 'Теплоёмкость(Р), кДж/кг*K: ' + str(round(PropsSI('C', 'T', float(dataT)+A, 'P', float(dataP)*B, 'IF97::Water') / 1000, 3))
                self.lpt.text = 'Коэф теплопроводности, Вт/м*К: ' + str(round(PropsSI('L', 'T', float(dataT)+A, 'P', float(dataP)*B, 'IF97::Water'), 4))
                self.vpt.text = 'Динамич. вязкость, Па*с: ' + str(round(PropsSI('V', 'T', float(dataT)+A, 'P', float(dataP)*B, 'IF97::Water'), 6))
                self.ppt.text = 'Число Прандтля: ' + str(round(PropsSI('Prandtl', 'T', float(dataT)+A, 'P', float(dataP)*B, 'IF97::Water'), 3))
                if float(dataP) > Pcrit:
                    self.phase.text = 'СКД'
                else:
                    if h > hs:
                        self.phase.text = 'Пар'
                    else:
                        self.phase.text = 'Вода'
            else:
                self.input_dataT.text = ''
        else:
            self.input_dataP.text = ''



class fPH_Screen(Screen):
    def __init__(self, name="fPH"):
        super(fPH_Screen, self).__init__(name=name)
        self.fPT = Button(text='f(PT)', background_color='yellow', on_release=self.tofPT)
        self.fPH = Button(text='f(PH)', background_color='green', on_release=self.tofPH)
        self.fP = Button(text='f(P)', background_color='blue', on_release=self.tofP)
        self.fT = Button(text='f(T)', background_color='red', on_release=self.tofT)
        self.name_fPH = Button(text='Свойства воды и пара. Фунцкия от Давления и Энтальпии.', background_color='green')
        self.label1 = Button(text='Давление, бар')
        self.label2 = Button(text='Энтальпия, кДж/кг')
        self.tph = Button(text='Температура, оС')
        self.dph = Button(text='Плотность, кг/м3')
        self.cph = Button(text='Теплоёмкость(изобар), кДж/кг*K')
        self.lph = Button(text='Коэф теплопроводности, Вт/м*K')
        self.vph = Button(text='Динамич. вязкость, Па*с')
        self.pph = Button(text='Число Прандтля: ')
        self.phase = Button(text='Агрегатное состояние: ')
        self.xph = Button(text='Массовое паросодержание: ')
        self.input_dataP = TextInput(hint_text='Давление, бар', multiline=False, halign="center", input_filter='int')
        self.input_dataH = TextInput(hint_text='Энтальпия, кДж/кг', multiline=False, halign="center", input_filter='int')
        self.input_dataP.bind(text=self.on_text)
        self.input_dataH.bind(text=self.on_text)

        flfPH = FloatLayout(size=(20, 20))
        al1 = AnchorLayout(anchor_y='bottom')
        al2 = AnchorLayout(anchor_y='top')
        bl1 = BoxLayout()
        bl2 = BoxLayout()
        gl1 = GridLayout(cols=2, rows=8, size_hint=(1, 0.8))
        gl2 = GridLayout(cols=1, rows=2, size_hint=(1, 0.2))

        gl1.add_widget(self.label1)
        gl1.add_widget(self.label2)
        gl1.add_widget(self.input_dataP)
        gl1.add_widget(self.input_dataH)
        gl1.add_widget(self.tph)
        gl1.add_widget(self.dph)
        gl1.add_widget(self.cph)
        gl1.add_widget(self.lph)
        gl1.add_widget(self.vph)
        gl1.add_widget(self.pph)
        gl1.add_widget(self.phase)
        gl1.add_widget(self.xph)

        bl1.add_widget(self.fPT)
        bl1.add_widget(self.fPH)
        bl1.add_widget(self.fP)
        bl1.add_widget(self.fT)
        bl2.add_widget(self.name_fPH)

        gl2.add_widget(bl1)
        gl2.add_widget(bl2)

        al1.add_widget(gl1)
        al2.add_widget(gl2)
        flfPH.add_widget(al1)
        flfPH.add_widget(al2)

        self.add_widget(flfPH)

    def tofPT(self, fPT):
        self.manager.current = "fPT"

    def tofPH(self, fPH):
        self.manager.current = "fPH"

    def tofP(self, fP):
        self.manager.current = "fP"

    def tofT(self, fT):
        self.manager.current = "fT"

    def on_text(self, *args):
        A = 1000
        B = 100000
        C = 273.15
        Pcrit = 221
        Pmin = 1.2
        Pmax = 500
        Hmin = 10
        Hmax = 3800
        dataP = self.input_dataP.text
        dataH = self.input_dataH.text

        if dataP.isnumeric():
            try:
                if float(dataP) > Pmax:
                    dataP = str(Pmax)
                else:
                    dataP = self.input_dataP.text
                if float(dataP) < Pmin:
                    dataP = str(Pmin)
                else:
                    dataP = self.input_dataP.text
            except:
                dataP = str(Pmin)

            if dataH.isnumeric():
                try:
                    if float(dataH) > Hmax:
                        dataH = str(Hmax)
                    else:
                        dataH = self.input_dataH.text
                    if float(dataH) < Hmin:
                        dataH = str(Hmin)
                    else:
                        dataH = self.input_dataH.text
                except:
                    dataH = str(Hmin)
                try:
                    if float(dataP) <= Pcrit:
                        hw = PropsSI('H', 'P', float(dataP) * B, 'Q', 0, 'IF97::Water') / 1000
                        hs = PropsSI('H', 'P', float(dataP) * B, 'Q', 1, 'IF97::Water') / 1000

                        if float(dataH) < hs and float(dataH) > hw:
                            dw = PropsSI('D', 'P', float(dataP) * B, 'Q', 0, 'IF97::Water')
                            ds = PropsSI('D', 'P', float(dataP) * B, 'Q', 1, 'IF97::Water')
                            cw = PropsSI('C', 'P', float(dataP) * B, 'Q', 0, 'IF97::Water') / 1000
                            cs = PropsSI('C', 'P', float(dataP) * B, 'Q', 1, 'IF97::Water') / 1000
                            lw = PropsSI('L', 'P', float(dataP) * B, 'Q', 0, 'IF97::Water')
                            ls = PropsSI('L', 'P', float(dataP) * B, 'Q', 1, 'IF97::Water')
                            vw = PropsSI('V', 'P', float(dataP) * B, 'Q', 0, 'IF97::Water')
                            vs = PropsSI('V', 'P', float(dataP) * B, 'Q', 1, 'IF97::Water')
                            pw = PropsSI('Prandtl', 'P', float(dataP) * B, 'Q', 0, 'IF97::Water')
                            ps = PropsSI('Prandtl', 'P', float(dataP) * B, 'Q', 1, 'IF97::Water')
                            tp = PropsSI('T', 'P', float(dataP) * B, 'Q', 1, 'IF97::Water') - C
                            xph = (float(dataH) - hw) / (hs - hw)
                            self.xph.text = 'Массовое паросодержание: ' + str(round(xph, 2))
                            self.phase.text = 'Пароводяная смесь'
                            tph = tp
                            dph = ds * xph + dw * (1 - xph)
                            cph = cs * xph + cw * (1 - xph)
                            lph = ls * xph + lw * (1 - xph)
                            vph = vs * xph + vw * (1 - xph)
                            pph = ps * xph + pw * (1 - xph)
                            self.tph.text = 'Температура, оС: ' + str(round(tph, 1))
                            self.dph.text = 'Плотность, кг/м3: ' + str(round(dph, 2))
                            self.cph.text = 'Теплоёмкость(Р), кДж/кг*K: ' + str(round(cph, 3))
                            self.lph.text = 'Коэф теплопроводности, Вт/м*K: ' + str(round(lph, 4))
                            self.vph.text = 'Динамич. вязкость, Па*с: ' + str(round(vph, 6))
                            self.pph.text = 'Число Прандтля: ' + str(round(pph, 3))
                        else:
                            tph = PropsSI('T', 'H', float(dataH) * A, 'P', float(dataP) * B, 'IF97::Water') - C
                            dph = PropsSI('D', 'H', float(dataH)*A, 'P', float(dataP)*B, 'IF97::Water')
                            cph = PropsSI('C', 'H', float(dataH)*A, 'P', float(dataP)*B, 'IF97::Water') / 1000
                            lph = PropsSI('L', 'H', float(dataH)*A, 'P', float(dataP)*B, 'IF97::Water')
                            vph = PropsSI('V', 'H', float(dataH)*A, 'P', float(dataP)*B, 'IF97::Water')
                            pph = PropsSI('Prandtl', 'H', float(dataH)*A, 'P', float(dataP)*B, 'IF97::Water')
                            self.tph.text = 'Температура, оС: ' + str(round(tph, 1))
                            self.dph.text = 'Плотность, кг/м3: ' + str(round(dph, 2))
                            self.cph.text = 'Теплоёмкость(Р), кДж/кг*K: ' + str(round(cph, 3))
                            self.lph.text = 'Коэф теплопроводности, Вт/м*K: ' + str(round(lph, 4))
                            self.vph.text = 'Динамич. вязкость, Па*с: ' + str(round(vph, 6))
                            self.pph.text = 'Число Прандтля: ' + str(round(pph, 3))
                            if float(dataH) >= hs:
                                self.phase.text = 'Перегретый пар'
                                self.xph.text = 'Перегретый пар '
                            else:
                                self.phase.text = 'Вода'
                                self.xph.text = 'Вода'
                    else:
                        tph = PropsSI('T', 'H', float(dataH) * A, 'P', float(dataP) * B, 'IF97::Water') - C
                        dph = PropsSI('D', 'H', float(dataH) * A, 'P', float(dataP) * B, 'IF97::Water')
                        cph = PropsSI('C', 'H', float(dataH) * A, 'P', float(dataP) * B, 'IF97::Water') / 1000
                        lph = PropsSI('L', 'H', float(dataH) * A, 'P', float(dataP) * B, 'IF97::Water')
                        vph = PropsSI('V', 'H', float(dataH) * A, 'P', float(dataP) * B, 'IF97::Water')
                        pph = PropsSI('Prandtl', 'H', float(dataH) * A, 'P', float(dataP) * B, 'IF97::Water')
                        self.phase.text = 'Среда сверхкритических параметров'
                        self.tph.text = 'Температура, оС: ' + str(round(tph, 1))
                        self.dph.text = 'Плотность, кг/м3: ' + str(round(dph, 2))
                        self.cph.text = 'Теплоёмкость(Р), кДж/кг*K: ' + str(round(cph, 3))
                        self.lph.text = 'Коэф теплопроводности, Вт/м*K: ' + str(round(lph, 4))
                        self.vph.text = 'Динамич. вязкость, Па*с: ' + str(round(vph, 6))
                        self.pph.text = 'Число Прандтля: ' + str(round(pph, 3))
                        self.xph.text = 'Среда сверхкритических параметров'
                except:
                    self.phase.text = 'За границами программы'
                    self.tph.text = 'За границами программы'
                    self.dph.text = 'За границами программы'
                    self.cph.text = 'За границами программы'
                    self.lph.text = 'За границами программы'
                    self.vph.text = 'За границами программы'
                    self.pph.text = 'За границами программы'
                    self.xph.text = 'За границами программы'
            else:
                self.phase.text = 'За границами программы'
                self.tph.text = 'За границами программы'
                self.dph.text = 'За границами программы'
                self.cph.text = 'За границами программы'
                self.lph.text = 'За границами программы'
                self.vph.text = 'За границами программы'
                self.pph.text = 'За границами программы'
                self.xph.text = 'За границами программы'
        else:
            self.phase.text = 'За границами программы'
            self.tph.text = 'За границами программы'
            self.dph.text = 'За границами программы'
            self.cph.text = 'За границами программы'
            self.lph.text = 'За границами программы'
            self.vph.text = 'За границами программы'
            self.pph.text = 'За границами программы'
            self.xph.text = 'За границами программы'



class fP_Screen(Screen):
    def __init__(self, name="fP"):
        super(fP_Screen, self).__init__(name=name)
        self.fPT = Button(text='f(PT)', background_color='yellow', on_release=self.tofPT)
        self.fPH = Button(text='f(PH)', background_color='green', on_release=self.tofPH)
        self.fP = Button(text='f(P)', background_color='blue', on_release=self.tofP)
        self.fT = Button(text='f(T)', background_color='red', on_release=self.tofT)
        self.name_fP = Button(text='Свойства воды и пара на линии насыщения. Фунцкия от Давления.', background_color='blue')
        self.tp = Button(text='Температура насыщения, оС ')
        self.hwp = Button(text='Энтальпия воды, кДж/кг ')
        self.hsp = Button(text='Энтальпия пара, кДж/кг ')
        self.dwp = Button(text='Плотность воды, кг/м3 ')
        self.dsp = Button(text='Плотность пара, кг/м3 ')
        self.cwp = Button(text='Теплоёмкость(изобар) воды, кДж/кг*K ')
        self.csp = Button(text='Теплоёмкость(изобар) пара, кДж/кг*K ')
        self.lwp = Button(text='Коэф теплопроводности воды, Вт/м*K ')
        self.lsp = Button(text='Коэф теплопроводности пара, Вт/м*K ')
        self.vwp = Button(text='Динамич. вязкость воды, Па*с ')
        self.vsp = Button(text='Динамич. вязкость пара, Па*с ')
        self.pwp = Button(text='Число Прандтля воды ')
        self.psp = Button(text='Число Прандтля пара ')

        self.input_dataP = TextInput(hint_text='Давление насыщения, бар', multiline=False, halign="center", input_filter='int')
        self.input_dataP.bind(text=self.on_text)

        flfP = FloatLayout(size=(20, 20))
        al1 = AnchorLayout(anchor_y='bottom')
        al2 = AnchorLayout(anchor_y='top')
        gl1 = GridLayout(cols=2, rows=8, size_hint=(1, 0.8))
        gl2 = GridLayout(cols=1, rows=2, size_hint=(1, 0.2))
        bl1 = BoxLayout()
        bl2 = BoxLayout()

        gl1.add_widget(self.input_dataP)
        gl1.add_widget(self.tp)
        gl1.add_widget(self.hwp)
        gl1.add_widget(self.hsp)
        gl1.add_widget(self.dwp)
        gl1.add_widget(self.dsp)
        gl1.add_widget(self.cwp)
        gl1.add_widget(self.csp)
        gl1.add_widget(self.lwp)
        gl1.add_widget(self.lsp)
        gl1.add_widget(self.vwp)
        gl1.add_widget(self.vsp)
        gl1.add_widget(self.pwp)
        gl1.add_widget(self.psp)

        bl1.add_widget(self.fPT)
        bl1.add_widget(self.fPH)
        bl1.add_widget(self.fP)
        bl1.add_widget(self.fT)
        bl2.add_widget(self.name_fP)

        gl2.add_widget(bl1)
        gl2.add_widget(bl2)

        al1.add_widget(gl1)
        al2.add_widget(gl2)
        flfP.add_widget(al1)
        flfP.add_widget(al2)

        self.add_widget(flfP)

    def tofPT(self, fPT):
        self.manager.current = "fPT"
        with self.canvas.before:
            Color(.20, .33, .31, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def tofPH(self, fPH):
        self.manager.current = "fPH"
        with self.canvas.before:
            Color(.20, .13, .31, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def tofP(self, fP):
        self.manager.current = "fP"
        with self.canvas.before:
            Color(.44, .43, .41, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def tofT(self, fT):
        self.manager.current = "fT"

    def on_text(self, *args):
        A = 273.15
        B = 100000
        Pcrit = 221

        dataP = self.input_dataP.text
        if dataP.isnumeric():
            if float(dataP) < Pcrit:
                hw = PropsSI('H', 'P', float(dataP)*B, 'Q', 0, 'IF97::Water') / 1000
                hs = PropsSI('H', 'P', float(dataP)*B, 'Q', 1, 'IF97::Water') / 1000
                dw = PropsSI('D', 'P', float(dataP)*B, 'Q', 0, 'IF97::Water')
                ds = PropsSI('D', 'P', float(dataP)*B, 'Q', 1, 'IF97::Water')
                cw = PropsSI('C', 'P', float(dataP)*B, 'Q', 0, 'IF97::Water') / 1000
                cs = PropsSI('C', 'P', float(dataP)*B, 'Q', 1, 'IF97::Water') / 1000
                lw = PropsSI('L', 'P', float(dataP)*B, 'Q', 0, 'IF97::Water')
                ls = PropsSI('L', 'P', float(dataP)*B, 'Q', 1, 'IF97::Water')
                vw = PropsSI('V', 'P', float(dataP)*B, 'Q', 0, 'IF97::Water')
                vs = PropsSI('V', 'P', float(dataP)*B, 'Q', 1, 'IF97::Water')
                pw = PropsSI('Prandtl', 'P', float(dataP)*B, 'Q', 0, 'IF97::Water')
                ps = PropsSI('Prandtl', 'P', float(dataP)*B, 'Q', 1, 'IF97::Water')
                tp = PropsSI('T', 'P', float(dataP)*B, 'Q', 1, 'IF97::Water') - A

                self.hwp.text = 'Энтальпия вода, кДж/кг: ' + str(round(hw, 1))
                self.hsp.text = 'Энтальпия пар, кДж/кг: ' + str(round(hs, 1))
                self.dwp.text = 'Плотность вода, кг/м3: ' + str(round(dw, 1))
                self.dsp.text = 'Плотность пар, кг/м3: ' + str(round(ds, 1))
                self.cwp.text = 'Теплоёмкость(Р) вода, кДж/кг*K: ' + str(round(cw, 3))
                self.csp.text = 'Теплоёмкость(Р) пар, кДж/кг*K: ' + str(round(cs, 3))
                self.lwp.text = 'Коэф теплопроводн. вода, Вт/м*К: ' + str(round(lw, 4))
                self.lsp.text = 'Коэф теплопроводн. пар, Вт/м*К: ' + str(round(ls, 4))
                self.vwp.text = 'Динамич. вязкость вода, Па*с: ' + str(round(vw, 6))
                self.vsp.text = 'Динамич. вязкость пар, Па*с: ' + str(round(vs, 6))
                self.pwp.text = 'Число Прандтля вода: ' + str(round(pw, 3))
                self.psp.text = 'Число Прандтля пар: ' + str(round(ps, 3))
                self.tp.text = 'Температура насыщения, оС: ' + str(round(tp, 1))
            else:
                self.hwp.text = 'Сверхкритические параметры среды.'
                self.hsp.text = 'Сверхкритические параметры среды.'
                self.dwp.text = 'Сверхкритические параметры среды.'
                self.dsp.text = 'Сверхкритические параметры среды.'
                self.cwp.text = 'Сверхкритические параметры среды.'
                self.csp.text = 'Сверхкритические параметры среды.'
                self.lwp.text = 'Сверхкритические параметры среды.'
                self.lsp.text = 'Сверхкритические параметры среды.'
                self.vwp.text = 'Сверхкритические параметры среды.'
                self.vsp.text = 'Сверхкритические параметры среды.'
                self.pwp.text = 'Сверхкритические параметры среды.'
                self.psp.text = 'Сверхкритические параметры среды.'
                self.tp.text = 'Сверхкритические параметры среды.'
        else:
            self.input_dataP.text = ''



class fT_Screen(Screen):
    def __init__(self, name="fT"):
        super(fT_Screen, self).__init__(name=name)
        self.fPT = Button(text='f(PT)', background_color='yellow', on_release=self.tofPT)
        self.fPH = Button(text='f(PH)', background_color='green', on_release=self.tofPH)
        self.fP = Button(text='f(P)', background_color='blue', on_release=self.tofP)
        self.fT = Button(text='f(T)', background_color='red', on_release=self.tofT)
        self.name_fT = Button(text='Свойства воды и пара на линии насыщения. Фунцкия от Температуры.', background_color='red')
        self.pt = Button(text='Давление насыщения, бар ', font_size='15sp', markup=True)
        self.hwt = Button(text='Энтальпия воды, кДж/кг ')
        self.hst = Button(text='Энтальпия пара, кДж/кг ')
        self.dwt = Button(text='Плотность воды, кг/м3 ')
        self.dst = Button(text='Плотность пара, кг/м3 ')
        self.cwt = Button(text='Теплоёмкость(изобар) воды, кДж/кг*K ')
        self.cst = Button(text='Теплоёмкость(изобар) пара, кДж/кг*K ')
        self.lwt = Button(text='Коэф теплопроводности воды, Вт/м*K ')
        self.lst = Button(text='Коэф теплопроводность пара, Вт/м*K ')
        self.vwt = Button(text='Динамич. вязкость воды, Па*с ')
        self.vst = Button(text='Динамич. вязкость пара, Па*с ')
        self.pwt = Button(text='Число Прандтля воды ')
        self.pst = Button(text='Число Прандтля пара ')

        self.input_dataT = TextInput(hint_text='Температура насыщения, оС', multiline=False, halign="center", input_filter='int')
        self.input_dataT.bind(text=self.on_text)
        flfT = FloatLayout(size=(20, 20), cls=(0, 0))
        al1 = AnchorLayout(anchor_y='bottom')
        al2 = AnchorLayout(anchor_y='top')
        gl1 = GridLayout(cols=2, rows=8, size_hint=(1, 0.8), padding=2)
        gl2 = GridLayout(cols=1, rows=2, size_hint=(1, 0.2))
        bl1 = BoxLayout()
        bl2 = BoxLayout()

        gl1.add_widget(self.input_dataT)
        gl1.add_widget(self.pt)
        gl1.add_widget(self.hwt)
        gl1.add_widget(self.hst)
        gl1.add_widget(self.dwt)
        gl1.add_widget(self.dst)
        gl1.add_widget(self.cwt)
        gl1.add_widget(self.cst)
        gl1.add_widget(self.lwt)
        gl1.add_widget(self.lst)
        gl1.add_widget(self.vwt)
        gl1.add_widget(self.vst)
        gl1.add_widget(self.pwt)
        gl1.add_widget(self.pst)

        bl1.add_widget(self.fPT)
        bl1.add_widget(self.fPH)
        bl1.add_widget(self.fP)
        bl1.add_widget(self.fT)
        bl2.add_widget(self.name_fT)

        gl2.add_widget(bl1)
        gl2.add_widget(bl2)

        al1.add_widget(gl1)
        al2.add_widget(gl2)
        flfT.add_widget(al1)
        flfT.add_widget(al2)

        self.add_widget(flfT)

    def tofPT(self, fPT):
        self.manager.current = "fPT"

    def tofPH(self, fPH):
        self.manager.current = "fPH"

    def tofP(self, fP):
        self.manager.current = "fP"

    def tofT(self, fT):
        self.manager.current = "fT"

    def on_text(self, *args):
        A = 273.15
        B = 100000
        Tcrit = 373.9

        dataT = self.input_dataT.text
        if dataT.isnumeric():
            if float(dataT) < Tcrit:
                hw = PropsSI('H', 'T', float(dataT)+A, 'Q', 0, 'IF97::Water') / 1000
                hs = PropsSI('H', 'T', float(dataT)+A, 'Q', 1, 'IF97::Water') / 1000
                dw = PropsSI('D', 'T', float(dataT)+A, 'Q', 0, 'IF97::Water')
                ds = PropsSI('D', 'T', float(dataT)+A, 'Q', 1, 'IF97::Water')
                cw = PropsSI('C', 'T', float(dataT)+A, 'Q', 0, 'IF97::Water') / 1000
                cs = PropsSI('C', 'T', float(dataT)+A, 'Q', 1, 'IF97::Water') / 1000
                lw = PropsSI('L', 'T', float(dataT)+A, 'Q', 0, 'IF97::Water')
                ls = PropsSI('L', 'T', float(dataT)+A, 'Q', 1, 'IF97::Water')
                vw = PropsSI('V', 'T', float(dataT)+A, 'Q', 0, 'IF97::Water')
                vs = PropsSI('V', 'T', float(dataT)+A, 'Q', 1, 'IF97::Water')
                pw = PropsSI('Prandtl', 'T', float(dataT)+A, 'Q', 0, 'IF97::Water')
                ps = PropsSI('Prandtl', 'T', float(dataT)+A, 'Q', 1, 'IF97::Water')
                pt = PropsSI('P', 'T', float(dataT)+A, 'Q', 1, 'IF97::Water') / B

                self.hwt.text = 'Энтальпия вода, кДж/кг: ' + str(round(hw, 1))
                self.hst.text = 'Энтальпия пар, кДж/кг: ' + str(round(hs, 1))
                self.dwt.text = 'Плотность вода, кг/м3: ' + str(round(dw, 2))
                self.dst.text = 'Плотность пар, кг/м3: ' + str(round(ds, 2))
                self.cwt.text = 'Теплоёмкость(Р) вода, кДж/кг*K: ' + str(round(cw, 3))
                self.cst.text = 'Теплоёмкость(Р) пар, кДж/кг*K: ' + str(round(cs, 3))
                self.lwt.text = 'Коэф теплопровод. вода, Вт/м*К: ' + str(round(lw, 4))
                self.lst.text = 'Коэф теплопровод. пар, Вт/м*К: ' + str(round(ls, 4))
                self.vwt.text = 'Динамич. вязкость вода, Па*с: ' + str(round(vw, 6))
                self.vst.text = 'Динамич. вязкость пар, Па*с: ' + str(round(vs, 6))
                self.pwt.text = 'Число Прандтля вода: ' + str(round(pw, 3))
                self.pst.text = 'Число Прандтля пар: ' + str(round(ps, 3))
                self.pt.text = 'Давление насыщения, бар: ' + str(round(pt, 1))
            else:
                self.hwt.text = 'Сверхкритические параметры среды.'
                self.hst.text = 'Сверхкритические параметры среды.'
                self.dwt.text = 'Сверхкритические параметры среды.'
                self.dst.text = 'Сверхкритические параметры среды.'
                self.cwt.text = 'Сверхкритические параметры среды.'
                self.cst.text = 'Сверхкритические параметры среды.'
                self.lwt.text = 'Сверхкритические параметры среды.'
                self.lst.text = 'Сверхкритические параметры среды.'
                self.vwt.text = 'Сверхкритические параметры среды.'
                self.vst.text = 'Сверхкритические параметры среды.'
                self.pwt.text = 'Сверхкритические параметры среды.'
                self.pst.text = 'Сверхкритические параметры среды.'
                self.pt.text = 'Сверхкритические параметры среды.'
        else:
            self.input_dataT.text = ''




class Menu(Screen):
    def __init__(self, name="menu"):
        super(Menu, self).__init__(name=name)
        self.fPT = Button(text='f(PT)', background_color='yellow', on_release=self.tofPT)
        self.fPH = Button(text='f(PH)', background_color='green', on_release=self.tofPH)
        self.fP = Button(text='f(P)', background_color='blue', on_release=self.tofP)
        self.fT = Button(text='f(T)', background_color='red', on_release=self.tofT)
        self.wsp = Label(text='Калькулятор т/д свойств воды и пара')

        flMenu = FloatLayout(size=(20, 20))

        al1 = AnchorLayout(anchor_y='bottom')
        al2 = AnchorLayout(anchor_y='top')
        gl1 = GridLayout(cols=2, rows=8, size_hint=(1, 0.8), padding=2)
        gl2 = GridLayout(cols=4, rows=1, size_hint=(1, 0.2))

        gl1.add_widget(self.wsp)

        gl2.add_widget(self.fPT)
        gl2.add_widget(self.fPH)
        gl2.add_widget(self.fP)
        gl2.add_widget(self.fT)

        al1.add_widget(gl1)
        al2.add_widget(gl2)
        flMenu.add_widget(al1)
        flMenu.add_widget(al2)

        self.add_widget(flMenu)

    def tofPT(self, fPT):
        self.manager.current = "fPT"

    def tofPH(self, fPH):
        self.manager.current = "fPH"

    def tofP(self, fP):
        self.manager.current = "fP"

    def tofT(self, fT):
        self.manager.current = "fT"



class calcWSP(App):
    def build(self):
        ScrManager = ScreenManager(transition = FadeTransition())
        screens = [Menu(), fPT_Screen(), fPH_Screen(), fP_Screen(), fT_Screen()]
        for i in screens:
            ScrManager.add_widget(i)
        return ScrManager

app = calcWSP()
app.run()