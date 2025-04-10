import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [mensajes, setMensajes] = useState([]);
  const [nuevoMensaje, setNuevoMensaje] = useState("");

  useEffect(() => {
    axios.get("http://localhost:8000/api/mensajes/")
      .then(res => setMensajes(res.data))
      .catch(err => console.error(err));
  }, []);

  const enviarMensaje = () => {
    axios.post("http://localhost:8000/api/mensajes/", { contenido: nuevoMensaje })
      .then(res => {
        setMensajes([...mensajes, res.data]);
        setNuevoMensaje("");
      });
  };

  return (
    <div>
      <h1>Mensajes</h1>
      <ul>
        {mensajes.map((msg, i) => <li key={i}>{msg.contenido}</li>)}
      </ul>
      <input
        type="text"
        value={nuevoMensaje}
        onChange={e => setNuevoMensaje(e.target.value)}
      />
      <button onClick={enviarMensaje}>Enviar</button>
    </div>
  );
}

export default App;
