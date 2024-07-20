import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Main.css'; // Importar los estilos CSS
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';
import { scaleQuantize } from 'd3-scale';
import allCountries from './features.json';

function Main() {
    const [targets, setTargets] = useState([]);
    const [last_date, setLastDate] = useState(null);
    const [countries, setCountries] = useState([]);

    const navigate = useNavigate();

    useEffect(() => {
        fetch('http://192.168.1.36:8000/ddosia/actual/uniques')
            .then(response => response.json())
            .then(data => {
                setLastDate(data.date);
                setTargets(data.domains);
                setCountries(data.countries.map(country => country.toLowerCase()));
            })
            .catch(error => console.error('Error:', error));
    }, []);

    const colorScale = scaleQuantize()
        .domain([0, 1])
        .range([
            "#ffedea",
            "#ffcec5",
            "#ffad9f",
            "#ff8a75",
            "#ff5533",
            "#e2492d",
            "#be3d26",
            "#9a311f",
            "#782618"
        ]);

    const baseColor = "#636363"; // Color para países no destacados

    return (
        <div className='container mt-5'>
            <header className='mb-4'>
                <h1 className='mb-3'>NoName057(16): Últimos objetivos (Actualizado el {last_date})</h1>
                <button className='btn btn-primary w-100' onClick={() => navigate('/database')}>Acceder a la base de datos de NoName</button>
            </header>
            <ComposableMap data-tip='' projectionConfig={{ scale: 200 }} className='map'>
                <Geographies geography={allCountries}>
                    {({ geographies }) =>
                        geographies.map(geo => {
                            const isHighlighted = countries.includes(geo.properties.name.toLowerCase());
                            return (
                                <Geography
                                    key={geo.rsmKey}
                                    geography={geo}
                                    fill={isHighlighted ? colorScale(1) : baseColor}
                                />
                            );
                        })
                    }
                </Geographies>
            </ComposableMap>
            <div className="row text-center mt-4">
                {targets.map(target => (
                    <div key={target} className="col-md-4 mb-3">
                        <div className="card">
                            <div className="card-body">
                                {target}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Main;
