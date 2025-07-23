elif seleccion == "Libro Diario":
    empresa = st.session_state.get("empresa", "Empresa Desconocida")
    moneda = st.session_state.get("simbolo_moneda", "RD$")
    formato_fecha = st.session_state.get("formato_fecha", "dd/mm/yyyy")

    st.subheader(f"📒 Libro Diario - {empresa}")
    st.write(f"Formato de fecha: {formato_fecha} | Moneda: {moneda}")

    st.markdown("### ➕ Ingresar Nueva Transacción")
    ...
    # (todo el bloque nuevo completo)

    with st.form("form_libro_diario"):
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            fecha = st.text_input("Fecha", placeholder="Ej: 19/12/2024")
        with col2:
            cuenta = st.text_input("Cuenta", placeholder="Ej: 101")
        with col3:
            descripcion = st.text_input("Descripcion", placeholder="Ej: Caja general")

        col4, col5 = st.columns(2)
        with col4:
            debe = st.text_input("Debe", placeholder="0.00")
        with col5:
            haber = st.text_input("Haber", placeholder="0.00")

        submit = st.form_submit_button("Agregar")

    # Simulador de "tabla de registros"
    if "asientos" not in st.session_state:
        st.session_state["asientos"] = []

    if submit:
        errores = []

        # Validaciones basicas
        if not fecha.replace("/", "").isdigit():
            errores.append("La fecha debe contener solo numeros y '/'.")
        if not cuenta.strip():
            errores.append("La cuenta no puede estar vacia.")
        if not descripcion.strip():
            errores.append("La descripcion no puede estar vacia.")
        try:
            valor_debe = float(debe) if debe.strip() else 0.0
        except:
            errores.append("Debe contiene un valor invalido.")
            valor_debe = 0.0
        try:
            valor_haber = float(haber) if haber.strip() else 0.0
        except:
            errores.append("Haber contiene un valor invalido.")
            valor_haber = 0.0

        if errores:
            st.error("⚠️ Errores encontrados:\n- " + "\n- ".join(errores))
        else:
            # Guardar en la sesion
            st.session_state["asientos"].append({
                "fecha": fecha,
                "cuenta": cuenta,
                "descripcion": descripcion,
                "debe": valor_debe,
                "haber": valor_haber
            })
            st.success("✅ Transaccion agregada con exito.")

    # Mostrar tabla actual
    if st.session_state["asientos"]:
        st.markdown("### 🧾 Asientos Registrados")
        total_debe = 0
        total_haber = 0

        for i, asiento in enumerate(st.session_state["asientos"], start=1):
            st.write(f"{i}. {asiento['fecha']} | {asiento['cuenta']} | {asiento['descripcion']} | {moneda} {asiento['debe']:,.2f} | {moneda} {asiento['haber']:,.2f}")
            total_debe += asiento["debe"]
            total_haber += asiento["haber"]

        st.markdown("---")
        st.write(f"🔢 **Total Debe:** {moneda} {total_debe:,.2f}")
        st.write(f"🔢 **Total Haber:** {moneda} {total_haber:,.2f}")

        if total_debe == total_haber:
            st.success("✅ Asiento Cuadrado.")
        else:
            st.warning("⚠️ Asiento no cuadrado. Verifique los valores.")

    else:
        st.info("No se han ingresado transacciones aun.")
