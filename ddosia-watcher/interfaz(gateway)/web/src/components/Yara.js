import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

function Yara() {
  const { hostId } = useParams();
  const [yaraRules, setYaraRules] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchYaraRules = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`http://192.168.1.36:8000/ddosia/yara?host_id=${hostId}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.text();
        setYaraRules(data); // Asumiendo que la respuesta incluye las reglas como texto plano
      } catch (error) {
        console.error('Error:', error);
        setYaraRules('No se pudo cargar las reglas SNORT');
      } finally {
        setIsLoading(false);
      }
    };

    fetchYaraRules();
  }, [hostId]);

  const copyToClipboard = () => {
    console.log('Clipboard API available:', navigator.clipboard);
    if (navigator.clipboard) {
      navigator.clipboard.writeText(yaraRules).then(() => {
        alert('reglas SNORT copiadas al portapapeles');
      }, (err) => {
        alert('Error al copiar las reglas SNORT: ', err);
      });
    } else {
      alert('Sin acceso a la API del portapapeles');
    }
  };
  

  if (isLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: "100vh" }}>
        <div className="spinner-border text-primary" role="status">
          <span className="sr-only">Cargando...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Reglas SNORT</h1>
      <button className="btn btn-primary mb-3" onClick={copyToClipboard}>Copiar al Portapapeles</button>
      <pre style={{width:'90%', height:'60%', margin:'auto'}}>{yaraRules}</pre>
    </div>
  );
}

export default Yara;
