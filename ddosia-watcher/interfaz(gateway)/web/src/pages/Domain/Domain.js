import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './Domain.css'; // Asegúrate de importar el archivo CSS

function Domain() {
  const { requestdomain } = useParams();
  const [domainID, setDomainID] = useState('Desconocido');
  const [regData, setDomainData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    console.log(`http://192.168.1.36:8000/ddosia/regs?host=${requestdomain}`);
    fetch(`http://192.168.1.36:8000/ddosia/regs?host=${requestdomain}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setDomainID(data.domains[0].host_id);
        const parsedData = data.domains.map(reg => ({
          ...reg,
          schema: JSON.parse(reg.schema)
        }));
        setDomainData(parsedData || []);
      })
      .catch(error => console.error('Error:', error));
  }, [requestdomain]);

  // Función para abrir una nueva ventana
  function openYaraRules() {
    window.open(`/database/yara/${domainID}`, '_blank');
  }

  return (
    <div>
      <div className="header-container">
        <h1>{requestdomain} [{domainID}]</h1>
        <button className="btn btn-primary btn-yara" onClick={openYaraRules}>Perfil SNORT</button>
      </div>
      {regData.length > 0 ? (
        regData.map(reg => (
          <div className='reg' key={reg.request_id} onClick={() => navigate(`/database/reg/${reg.request_id}`)}>
            <p>Request ID: {reg.request_id}</p>
            <p>IP: {reg.schema.ip}</p>
            <p>Path: {reg.schema.path}</p>
            <p>Method: {reg.schema.method}</p>
          </div>
        ))
      ) : (
        <p className="no-data">No hay datos disponibles.</p>
      )}
    </div>
  );
}

export default Domain;
