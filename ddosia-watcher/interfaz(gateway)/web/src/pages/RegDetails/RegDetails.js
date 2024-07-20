import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './RegDetails.css';  // Importa los estilos CSS

function RegDetails() {
  const { requestId } = useParams();
  const [regData, setDomainData] = useState(null);
  const [YARA_rule, setYARA] = useState(null);
  useEffect(() => {
    fetch(`http://192.168.1.36:8000/ddosia/regs?request_id=${requestId}`)
      .then(response => response.json())
      .then(data => {
        if (data.domains && data.domains.length > 0) {
          const domainData = data.domains[0];
          if (domainData.schema && typeof domainData.schema === 'string') {
            domainData.schema = JSON.parse(domainData.schema);
          }
          setDomainData(domainData);
        }
      })
      .catch(error => console.error('Error:', error));

      fetch(`http://192.168.1.36:8000/ddosia/yara?request_id=${requestId}`)
      .then(response => response.text())
      .then(data => {
        console.log(data);
        setYARA(data)
      })
      .catch(error => console.error('Error:', error));
  }, [requestId]);

  return (
    <div className="RegDetails">
      {regData ? (
        <div>
          <h2 className="header">Dominio: {regData.host}</h2>
          <div className="details">
            <p>Host ID: {regData.host_id}</p>
            <p>Request ID: {regData.request_id}</p>
            <p>Última vez visto: {regData.last_time_seen}</p>
          </div>
          <h3>Esquema:</h3>
          <pre className="pre-json">
            {JSON.stringify(regData.schema, null, 2)}
          </pre>
          <hr></hr>
          <h3>Regla SNORT</h3>
          <pre>
            {YARA_rule}
          </pre>
        </div>
      ) : (
        <p className="loading">Cargando...</p>
      )}
    </div>
  );
}

export default RegDetails;
