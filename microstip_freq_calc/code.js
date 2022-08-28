var msEr;  			// Substrate dielectric constant
        var msEeff; 		// Effective dielectric constant
        var msTand; 		// Dielectric loss tangent
        var msRho;        	// Resistivity of the conductor relative to copper. (i.e, a copper conductor has a Rho of 1)
        var msHeight; 	// Substrate height. Note: In the MS equations this is H and in the Stripline equtsions, this is B
        var msThickness; 	// Thickness of the conductor
        var msWidth; 	// Width of the conductor
        var msLength; 	// Length of the conductor
        var msZo; 		// Characteristic impedance of the transmission line
        var msAngle; 	// Electrical length of the transmission line at the given frequency in degress
        var msFreq; 		// Frequency of which the transmission line is evaluated
        var msLoss; 		// Loss of the transmission line in dB at the specified length and frequency

        var ms_c = 2.997925e8; // speed of light in meters / second
        var msmpm = 39370.07874; // mils per meter
        var ms_fsmu = 4.0 * Math.PI * 1.0e-7; // freespace mu
        var ms_rc = 5.96e7; // conductivity of copper.
        var msZofn = 59.9585;

        var ms_default_sel_height = 0; 		// change these values to change default dimension/frequency unit selectors
        var ms_default_sel_thickness = 0; 	// 0=mils, 1=inches, 2=mm, 3=cm
        var ms_default_sel_freq = 0;
        var ms_default_sel_width = 0;
        var ms_default_sel_length = 0;

        var ms_cur_sel_height = ms_default_sel_height;
        var ms_cur_sel_thickness = ms_default_sel_thickness;
        var ms_cur_sel_freq = ms_default_sel_freq;
        var ms_cur_sel_width = ms_default_sel_width;
        var ms_cur_sel_length = ms_default_sel_length;

        var msUnits = ["mils", "Inches", "mm", "cm"];
        var msUnitsVal = [1.0, 1000.0, 1, 10];
        var msFreqUnits = ["GHz", "MHz", "kHz", "Hz"];
        var msFreqUnitsVal = [1, .001, .000001, .000000001];

        //msAnalyze();

        function msInitDefaultValues() {
            // change these values to your desired default values.
            msEr = 3.66;
            msTand = .002;
            msRho = 1.0;
            msHeight = 20;
            msThickness = 1.4;
            msWidth = 45;
            msLength = 750;
            msFreq = 2.45;
        }

        function msSetup() {
            msInitDefaultValues();
            msSetFormValues();
            msSetSelectorOptions();

            document.getElementById('edt_msEeff').readOnly = true;
            document.getElementById('edt_msLoss').readOnly = true;
            msAnalyze();
        }

        function msSetSelectorOptions() {
            var selectHeight = document.getElementById("sel_msHeight");
            var selectThickness = document.getElementById("sel_msThickness");
            var selectFreq = document.getElementById("sel_msFreq");
            var selectWidth = document.getElementById("sel_msWidth");
            var selectLength = document.getElementById("sel_msLength");

            for (var i = 0; i < msUnits.length; i++) {
                var option = document.createElement("option");
                option.value = i;
                option.text = msUnits[i];
                selectHeight.appendChild(option);
            }
            selectHeight.value = ms_default_sel_height;
            selectHeight.onfocus = function () { msSelectFocus("height", selectHeight); }
            selectHeight.onchange = function () { msSelectChange("height", selectHeight); }

            for (var i = 0; i < msUnits.length; i++) {
                var option = document.createElement("option");
                option.value = i;
                option.text = msUnits[i];
                selectThickness.appendChild(option);
            }
            selectThickness.value = ms_default_sel_thickness;
            selectThickness.onfocus = function () { msSelectFocus("thickness", selectThickness); }
            selectThickness.onchange = function () { msSelectChange("thickness", selectThickness); }

            for (var i = 0; i < msFreqUnits.length; i++) {
                var option = document.createElement("option");
                option.value = i;
                option.text = msFreqUnits[i];
                selectFreq.appendChild(option);
            }
            selectFreq.value = ms_default_sel_freq;
            selectFreq.onfocus = function () { msSelectFocus("freq", selectFreq); }
            selectFreq.onchange = function () { msSelectChange("freq", selectFreq); }

            for (var i = 0; i < msUnits.length; i++) {
                var option = document.createElement("option");
                option.value = i;
                option.text = msUnits[i];
                selectWidth.appendChild(option);
            }
            selectWidth.value = ms_default_sel_width;
            selectWidth.onfocus = function () { msSelectFocus("width", selectWidth); }
            selectWidth.onchange = function () { msSelectChange("width", selectWidth); }

            for (var i = 0; i < msUnits.length; i++) {
                var option = document.createElement("option");
                option.value = i;
                option.text = msUnits[i];
                selectLength.appendChild(option);
            }
            selectLength.value = ms_default_sel_length;
            selectLength.onfocus = function () { msSelectFocus("length", selectLength); }
            selectLength.onchange = function () { msSelectChange("length", selectLength); }
        }

        function msSelectFocus(str, selector) {
            if (str == "height")
                ms_cur_sel_height = selector.value;
            else if (str == "thickness")
                ms_cur_sel_thickness = selector.value;
            else if (str == "freq")
                ms_cur_sel_freq = selector.value;
            else if (str == "width")
                ms_cur_sel_width = selector.value;
            else
                ms_cur_sel_length = selector.value;
        }

        function msSelectChange(str, selector) {
            if (str == "height") {
                if (msIsNumber(document.getElementById('edt_msHeight').value))
                    msConvertHeight();
                ms_cur_sel_height = selector.value;
            }
            else if (str == "thickness") {
                if (msIsNumber(document.getElementById('edt_msThickness').value))
                    msConvertThickness();
                ms_cur_sel_thickness = selector.value;
            }
            else if (str == "freq") {
                if (msIsNumber(document.getElementById('edt_msFreq').value))
                    msConvertFrequency();
                ms_cur_sel_freq = selector.value;
            }
            else if (str == "width") {
                if (msIsNumber(document.getElementById('edt_msWidth').value))
                    msConvertWidth();
                ms_cur_sel_width = selector.value;
            }
            else {
                if (msIsNumber(document.getElementById('edt_msLength').value))
                    msConvertLength();
                ms_cur_sel_length = selector.value;
            }
        }

        function msConvertHeight() {
            var selectHeight = document.getElementById("sel_msHeight");

            msHeight = document.getElementById('edt_msHeight').value;

            if ((ms_cur_sel_height < 2 && selectHeight.value < 2) || (ms_cur_sel_height > 1 && selectHeight.value > 1)) {
                msHeight = msHeight * msUnitsVal[ms_cur_sel_height] / msUnitsVal[selectHeight.value];
            }
            else {
                if (ms_cur_sel_height < 2)
                    msHeight = msHeight * msUnitsVal[ms_cur_sel_height] * 1000 / (msUnitsVal[selectHeight.value] * msmpm);
                else
                    msHeight = msHeight * msmpm * (msUnitsVal[ms_cur_sel_height] / (msUnitsVal[selectHeight.value] * 1000));
            }
            msDisplayHeight(5);
        }

        function msConvertThickness() {
            var selected = document.getElementById("sel_msThickness");
            msThickness = document.getElementById('edt_msThickness').value;
            if ((ms_cur_sel_thickness < 2 && selected.value < 2) || (ms_cur_sel_thickness > 1 && selected.value > 1)) {
                msThickness = msThickness * msUnitsVal[ms_cur_sel_thickness] / msUnitsVal[selected.value];
            }
            else {
                if (ms_cur_sel_thickness < 2)
                    msThickness = msThickness * msUnitsVal[ms_cur_sel_thickness] * 1000 / (msUnitsVal[selected.value] * msmpm);
                else
                    msThickness = msThickness * msmpm * (msUnitsVal[ms_cur_sel_thickness] / (msUnitsVal[selected.value] * 1000));
            }
            msDisplayThickness(5);
        }

        function msConvertWidth() {
            var selected = document.getElementById("sel_msWidth");
            msWidth = document.getElementById('edt_msWidth').value;
            if ((ms_cur_sel_width < 2 && selected.value < 2) || (ms_cur_sel_width > 1 && selected.value > 1)) {
                msWidth = msWidth * msUnitsVal[ms_cur_sel_width] / msUnitsVal[selected.value];
            }
            else {
                if (ms_cur_sel_width < 2)
                    msWidth = msWidth * msUnitsVal[ms_cur_sel_width] * 1000 / (msUnitsVal[selected.value] * msmpm);
                else
                    msWidth = msWidth * msmpm * (msUnitsVal[ms_cur_sel_width] / (msUnitsVal[selected.value] * 1000));
            }
            msDisplayWidth(5);
        }

        function msConvertLength() {
            var selected = document.getElementById("sel_msLength");
            msLength = document.getElementById('edt_msLength').value;
            if ((ms_cur_sel_length < 2 && selected.value < 2) || (ms_cur_sel_length > 1 && selected.value > 1)) {
                msLength = msLength * msUnitsVal[ms_cur_sel_length] / msUnitsVal[selected.value];
            }
            else {
                if (ms_cur_sel_length < 2)
                    msLength = msLength * msUnitsVal[ms_cur_sel_length] * 1000 / (msUnitsVal[selected.value] * msmpm);
                else
                    msLength = msLength * msmpm * (msUnitsVal[ms_cur_sel_length] / (msUnitsVal[selected.value] * 1000));
            }
            msDisplayLength(5);
        }

        function msConvertFrequency() {
            var selected = document.getElementById("sel_msFreq");
            msFreq = document.getElementById('edt_msFreq').value;
            msFreq = msFreq * msFreqUnitsVal[ms_cur_sel_freq] / msFreqUnitsVal[selected.value];
            msDisplayFreq();
        }

        function msLoadSubstrateValues() {
            msEr = parseFloat(document.getElementById('edt_msEr').value);
            msTand = parseFloat(document.getElementById('edt_msTand').value);
            msRho = parseFloat(document.getElementById('edt_msRho').value);
            msHeight = parseFloat(document.getElementById('edt_msHeight').value);
            msThickness = parseFloat(document.getElementById('edt_msThickness').value);
            msFreq = parseFloat(document.getElementById('edt_msFreq').value);
        }

        function msLoadAnalyzeValues() {
            msWidth = parseFloat(document.getElementById('edt_msWidth').value);
            msLength = parseFloat(document.getElementById('edt_msLength').value);
        }

        function msLoadSynthesizeValues() {
            msZo = parseFloat(document.getElementById('edt_msZo').value);
            msAngle = parseFloat(document.getElementById('edt_msAngle').value);
        }

        function msSetFormValues() {
            document.getElementById('edt_msEr').value = msEr;
            document.getElementById('edt_msTand').value = msTand;
            document.getElementById('edt_msRho').value = msRho;
            document.getElementById('edt_msHeight').value = msHeight;
            document.getElementById('edt_msThickness').value = msThickness;
            document.getElementById('edt_msWidth').value = msWidth;
            document.getElementById('edt_msLength').value = msLength;
            document.getElementById('edt_msFreq').value = msFreq;
        }

        function msAnalyze() {
            msLoadSubstrateValues();
            msLoadAnalyzeValues();
            if (msCheckSubstrateValues() && msCheckAnalyzeValues()) {
                var h = msGetHeight();
                var t = msGetThickness();
                var w = msGetWidth();
                var l = msGetLength();
                var f = msConvertFreqToHz();

                msCalcZo(h, t, w, f);
                msCalcAngle(l);
                msLoss = (msCalcConductorLoss(msConvertFreqToHz(), h, t, w) + msCalcDielectricLoss(msConvertFreqToHz()) / msmpm) * l;

                msDisplayZo(2);
                msDisplayAngle(2);
                msDisplayLoss(3);
                msDisplayEeff(3);
            }
        }

        function msSynthesize() {
            msLoadSubstrateValues();
            msLoadSynthesizeValues();
            if (msCheckSubstrateValues() && msCheckSynthesizeValues()) {
                var h = msGetHeight();
                var t = msGetThickness();
                var w, l;
                w = msCalcWidth(h, t);
                l = msCalcLength();
                msLoss = (msCalcConductorLoss(msConvertFreqToHz(), h, t, w) + msCalcDielectricLoss(msConvertFreqToHz()) / msmpm) * l;
                msSetWidth(w);
                msSetLength(l);
                msDisplayWidth(5);
                msDisplayLength(5);
                msDisplayLoss(3);
            }
        }

        function coth2(x) {
            var retVal;
            retVal = ((Math.exp(x) + Math.exp(-x)) / 2.0) / ((Math.exp(x) - Math.exp(-x)) / 2.0);
            return retVal * retVal;
        }

        function msCalcZo(h, t, w, f) {
            var u, u1, ur, dur, du1;
            var tu, eff0 = 0.0, fn;
            var p, p1, p2, p3, p4;
            var r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17;
            var Zo;
            u = w / h;
            du1 = 0;
            dur = 0;
            if (t > 0) {
                tu = t / h;
                du1 = (tu / Math.PI) * Math.log1p(4.0 * Math.E / (tu * coth2(Math.pow(6.517 * u, 0.5))));
                dur = 0.5 * (1.0 + 1.0 / Math.cosh(Math.pow(msEr - 1.0, 0.5))) * du1;
            }

            u1 = u + du1;
            ur = u + dur;
            Zo = Zo1(ur) / Math.pow(msCalcEeff(ur, msEr), 0.5);
            eff0 = msCalcEeff(ur, msEr) * Math.pow(Zo1(u1) / Zo1(ur), 2.0);
            fn = f * h * 0.0254 / 1.0e9;
            p1 = 0.27488 + u * (0.6315 + 0.525 / Math.pow(1.0 + 0.0157 * fn, 20.0)) - 0.065683 * Math.exp(-8.7513 * u);
            p2 = 0.33622 * (1.0 - Math.exp(-0.03442 * msEr));
            p3 = 0.0363 * Math.exp(-4.6 * u) * (1.0 - Math.exp(-1.0 * Math.pow(fn / 3.87, 4.97)));
            p4 = 2.751 * (1.0 - Math.exp(-1.0 * Math.pow(msEr / 15.916, 8.0))) + 1.0;
            p = p1 * p2 * Math.pow(fn * (0.1844 + p3 * p4), 1.5763);
            msEeff = (eff0 + msEr * p) / (1.0 + p);
            r1 = 0.03891 * Math.pow(msEr, 1.4);
            r2 = 0.267 * Math.pow(u, 7.0);
            r3 = 4.766 * Math.exp(-3.228 * Math.pow(ur, 0.641));
            r4 = 0.016 + Math.pow(0.0514 * msEr, 4.524);
            r5 = Math.pow(fn / 28.843, 12.0);
            r6 = 22.2 * Math.pow(ur, 1.92);
            r7 = 1.206 - 0.3144 * Math.exp(-r1) * (1.0 - Math.exp(-r2));
            r8 = 1.0 + 1.275 * (1.0 - Math.exp(-0.004625 * r3 * Math.pow(msEr, 1.674) * Math.pow(fn / 18.365, 2.745)));
            r9 = (5.086 * r4 * r5 / (0.3838 + 0.386 * r4)) * (Math.exp(-r6) / (1.0 + 1.2992 * r5)) * Math.pow(msEr - 1.0, 6.0) / (1.0 + 10.0 * Math.pow(msEr - 1.0, 6.0));
            r10 = 0.00044 * Math.pow(msEr, 2.136) + 0.0184;
            r11 = Math.pow(fn / 19.47, 6.0) / (1.0 + 0.0962 * Math.pow(fn / 19.47, 6.0));
            r12 = 1.0 / (1.0 + 0.00245 * u * u);
            r13 = 0.9408 * Math.pow(msEeff, r8) - 0.9603;
            r14 = (0.9408 - r9) * Math.pow(eff0, r8) - 0.9603;
            r15 = 0.707 * r10 * Math.pow(fn / 12.3, 1.097);
            r16 = 1.0 + 0.0503 * msEr * msEr * r11 * (1.0 - Math.exp(-1.0 * Math.pow(u / 15.0, 6.0)));
            r17 = r7 * (1.0 - 1.1241 * (r12 / r16) * Math.exp(-0.026 * Math.pow(fn, 1.15656) - r15));
            msZo = Zo * Math.pow(r13 / r14, r17);
        }

        function msCalcEeff(u, er) {
            // source: Hammerstad and Jensen, "Accurate Models for Microstrip Computer Aided Design", 1980 IEEE MTT-S International Microwave Symposium Digest
            // 		   R.K. Hoffman, Handbook of Microwave integrated Circuits, 1987 for the impedance dispersion curve fit.

            var a = 0.0;
            var b = 0.0;
            var ef = 0.0;
            a = 1.0 + Math.log((Math.pow(u, 4.0) + Math.pow(u / 52.0, 2.0)) / (Math.pow(u, 4.0) + 0.432)) / 49.0 + Math.log1p(Math.pow(u / 18.1, 3)) / 18.7;
            b = 0.564 * Math.pow((er - 0.9) / (er + 3.0), 0.053);
            ef = (er + 1.0) / 2.0 + ((er - 1) / 2.0) * Math.pow((1.0 + 10.0 / u), -1.0 * a * b);
            return ef;
        }

        function Zo1(u) {
            var f = 0.0;
            var z = 0.0;
            f = 6.0 + (2.0 * Math.PI - 6.0) * Math.exp(-1.0 * Math.pow((30.666 / u), 0.7528));
            z = msZofn * Math.log(f / u + Math.pow(1.0 + 4.0 / (u * u), 0.5));
            return z;
        }

        function msCalcWidth(h, t) {
            var u, du, u1, u2, u3, u4;
            var v1, v2, v3, v4;
            var Zc;
            u = 0.1;
            du = 0.5;
            Zc = msZo;
            v1 = getV(h, t, u, Zc);
            u += du;
            v2 = getV(h, t, u, Zc);
            while (v1 * v2 > 0) {
                v1 = v2;
                u += du;
                v2 = getV(h, t, u, Zc);
            }
            u2 = u;
            u1 = u - du;
            u = u1 + (u2 - u1) * 0.381966;
            u3 = u;
            v3 = Math.abs(getV(h, t, u, Zc));
            u = u1 + (u2 - u1) / 1.618034;
            u4 = u;
            v4 = Math.abs(getV(h, t, u4, Zc));
            var Zerr = Zc / 10000.0
            while ((v3 + v4) > Zerr) {
                if (v3 > v4) {
                    u1 = u3;
                    u3 = u4;
                    v3 = v4;
                    u = u1 + (u2 - u1) / 1.618034;
                    u4 = u;
                    v4 = Math.abs(getV(h, t, u, Zc));
                }
                else {
                    u2 = u4;
                    u4 = u3;
                    v4 = v3;
                    u = u1 + (u2 - u1) * 0.381966;
                    u3 = u;
                    v3 = Math.abs(getV(h, t, u, Zc));
                }
            }
            u = (u1 + u2) / 2;
            return u * h;
        }

        function getV(h, t, u, z) {
            var v;
            var w;
            w = u * h
            msCalcZo(h, t, w, msConvertFreqToHz());
            v = msZo - z;
            return v;
        }

        function msCalcLength()
        { return (msAngle / 360.0) * msCalcWavelength(msConvertFreqToHz()) * msmpm; }

        function msCalcAngle(l)
        { msAngle = (l * 360.0) / (msCalcWavelength(msConvertFreqToHz()) * msmpm); }

        function msCalcWavelength(freq)
        { return ms_c / (freq * Math.pow(msEeff, 0.5)); }

        function msCalcWavelengthEr(freq, er)
        { return ms_c / (freq * Math.pow(er, 0.5)); }

        function msCalcDielectricLoss(freq) {
            // dielectric loss in db / meter
            // freq = frequency in Hz
            // source: Gupta, "Computer-Aided Design of Microwave Circuits" p. 65
            var dloss = 27.3 * (msEr / (msEr - 1.0)) * ((msEeff - 1.0) / Math.pow(msEeff, 0.5)) * (msTand * msConvertFreqToHz() / ms_c);
            return dloss;
        }

        function msCalcConductorLoss(freq, h, t, w) {
            // conductor loss in db / meter
            // freq = frequency in Hz
            // source: Gupta, "Computer-Aided Design of Microwave Circuits" p. 64

            var ac, u, a, b, rs, rel;
            var tu, du1, dur, ur;
            u = w / h;
            rel = msRho / ms_rc;
            dur = 0.0;
            if (t > 0.0) {
                tu = t / h;
                du1 = (tu / Math.PI) * Math.log1p(4.0 * Math.E / (tu * coth2(Math.pow(6.517 * u, 0.5))));
                dur = 0.5 * (1.0 + 1.0 / Math.cosh(Math.pow(msEr - 1.0, 0.5))) * du1;
            }
            ur = u + dur;
            if (u >= 1.0 / (2 * Math.PI))
                b = h;
            else
                b = 2 * Math.PI * w;
            rs = Math.pow(Math.PI * msConvertFreqToHz() * ms_fsmu * rel, 0.5);
            if (t > 0)
                a = 1.0 + (1.0 + Math.log(2 * b / t) / Math.PI) / ur;
            else
                a = 1.0;
            if (u <= 1.0)
                ac = 1.38 * a * (rs / (h * msZo)) * (32.0 - ur * ur) / (32.0 + ur * ur);
            else
                ac = 6.1e-5 * a * (rs * msZo * msEeff / h) * (u + (0.667 * ur / (ur + 1.444)));
            return ac;
        }

        function msDisplayHeight(precision)
        { document.getElementById('edt_msHeight').value = msHeight.toFixed(precision); }

        function msDisplayThickness(precision)
        { document.getElementById('edt_msThickness').value = msThickness.toFixed(precision); }

        function msDisplayFreq()
        { document.getElementById('edt_msFreq').value = msFreq; }

        function msDisplayZo(precision)
        { document.getElementById('edt_msZo').value = msZo.toFixed(precision); }

        function msDisplayAngle(precision)
        { document.getElementById('edt_msAngle').value = msAngle.toFixed(precision); }

        function msDisplayLoss(precision)
        { document.getElementById('edt_msLoss').value = msLoss.toFixed(precision); }

        function msDisplayEeff(precision)
        { document.getElementById('edt_msEeff').value = msEeff.toFixed(precision); }

        function msDisplayWidth(precision)
        { document.getElementById('edt_msWidth').value = parseFloat(msWidth).toFixed(precision); }

        function msDisplayLength(precision)
        { document.getElementById('edt_msLength').value = msLength.toFixed(precision); }

        function msCheckSubstrateValues() {
            if (!msIsNumber(document.getElementById('edt_msEr').value)) {
                msErrorNotNumeric("\u03B5r");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msEr').value) >= 1.0)) {
                msErrorNotGTE1("\u03B5r");
                return false;
            }
            if (!msIsNumber(document.getElementById('edt_msTand').value)) {
                msErrorNotNumeric("Tan\u03B4");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msTand').value) >= 0)) {
                msErrorNotGTEZ("Tan\u03B4");
                return false;
            }
            if (!msIsNumber(document.getElementById('edt_msRho').value)) {
                msErrorNotNumeric("Rho");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msRho').value) > 0)) {
                msErrorNotGTZ("Rho");
                return false;
            }
            if (!msIsNumber(document.getElementById('edt_msHeight').value)) {
                msErrorNotNumeric("Height");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msHeight').value) > 0)) {
                msErrorNotGTZ("Height");
                return false;
            }
            if (!msIsNumber(document.getElementById('edt_msThickness').value)) {
                msErrorNotNumeric("Thickness");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msThickness').value) >= 0)) {
                msErrorNotGTEZ("Thickness");
                return false;
            }
            if (!msIsNumber(document.getElementById('edt_msFreq').value)) {
                msErrorNotNumeric("Frequency");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msFreq').value) >= 0)) {
                msErrorNotGTEZ("Frequency");
                return false;
            }
            return true;
        }

        function msCheckAnalyzeValues() {
            if (!msIsNumber(document.getElementById('edt_msWidth').value)) {
                msErrorNotNumeric("Width");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msWidth').value) > 0)) {
                msErrorNotGTZ("Width");
                return false;
            }
            if (!msIsNumber(document.getElementById('edt_msLength').value)) {
                msErrorNotNumeric("Length");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msLength').value) > 0)) {
                msErrorNotGTZ("Length");
                return false;
            }
            return true;
        }

        function msCheckSynthesizeValues() {
            if (!msIsNumber(document.getElementById('edt_msZo').value)) {
                msErrorNotNumeric("Zo");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msZo').value) > 0)) {
                msErrorNotGTZ("Zo");
                return false;
            }
            if (!msIsNumber(document.getElementById('edt_msAngle').value)) {
                msErrorNotNumeric("Angle");
                return false;
            }
            else if (!(parseFloat(document.getElementById('edt_msAngle').value) > 0)) {
                msErrorNotGTZ("Angle");
                return false;
            }
            return true;
        }

        function msIsNumber(num)
        { return !isNaN(parseFloat(num)) && isFinite(num); }

        function msErrorNotNumeric(title)
        { alert("Error - " + title + " must be numeric."); }

        function msErrorNotGTZ(title)
        { alert("Error - " + title + " must be greater than zero."); }

        function msErrorNotGTEZ(title)
        { alert("Error - " + title + " must be greater than or equal to zero."); }

        function msErrorNotGTE1(title)
        { alert("Error - " + title + " must be greater than or equal to 1.0"); }

        function msCalcFromToMil(from) {
            if (from < 2)
                return msUnitsVal[from];

            return msmpm * msUnitsVal[from] / 1000.0;
        }

        function msCalcFromMilTo(to) {
            if (to < 2)
                return 1 / msUnitsVal[to];

            return 1000.0 / (msmpm * msUnitsVal[to]);
        }

        function msGetHeight()
        { return msHeight * msCalcFromToMil(ms_cur_sel_height); }

        function msGetThickness()
        { return msThickness * msCalcFromToMil(ms_cur_sel_thickness); }

        function msGetWidth()
        { return msWidth * msCalcFromToMil(ms_cur_sel_width); }

        function msSetWidth(w)
        { msWidth = w * msCalcFromMilTo(ms_cur_sel_width); }

        function msGetLength()
        { return msLength * msCalcFromToMil(ms_cur_sel_length); }

        function msSetLength(l)
        { msLength = l * msCalcFromMilTo(ms_cur_sel_length); }

        function msConvertFreqToHz()
        { return msFreq * msFreqUnitsVal[ms_cur_sel_freq] / .000000001; }