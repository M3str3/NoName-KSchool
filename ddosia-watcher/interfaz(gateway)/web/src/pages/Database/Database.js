import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import './Database.css'; // Importar los estilos

function Database() {
  const [domains, setDomains] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://192.168.1.36:8000/ddosia/domains/uniques')
      .then(response => response.json())
      .then(data => setDomains(data.domains))
      .catch(error => console.error('Error:', error));
  }, []);

  const filteredDomains = searchTerm
    ? domains.filter(domain => domain.host.toLowerCase().includes(searchTerm.toLowerCase()))
    : domains;

  const counts = {};
  filteredDomains.forEach(domain => {
    const ext = domain.host.split('.').pop();
    counts[ext] = counts[ext] ? counts[ext] + 1 : 1;
  });

  const data = Object.keys(counts).map(key => ({ name: key, value: counts[key] }));

  return (
    <div className={`container ${searchTerm ? 'active' : ''}`}>
      <h1>NoName Database</h1>
      <div className="chart-container">
        <PieChart width={400} height={400}>
          <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={150} fill="#8884d8">
            {data.map((entry, index) => <Cell key={`cell-${index}`} fill={["#0088FE", "#00C49F", "#FFBB28", "#FF8042"][index % 4]}/>)}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Buscar por host..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
        />
      </div>
      <div className="domains-container">
        {searchTerm && (filteredDomains.length > 0 ? (
          filteredDomains.map(domain => (
            <div key={domain.request_id} className="domain"
                 onClick={() => navigate(`/database/domain/${domain.host}`)}>
              <p>{domain.host}</p>
            </div>
          ))
        ) : (
          <div className="no-results">Sin resultados</div>
        ))}
      </div>
    </div>
  );
}

export default Database;
