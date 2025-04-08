<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Filtro Dual Amplifier Band-Pass</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #2980b9;
            margin-top: 20px;
        }
        .section {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        iframe, img {
            display: block;
            margin: 10px auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>Filtro Dual Amplifier Band-Pass</h1>

    <div class="section">
        <h2>Documentação do Projeto</h2>
        <iframe src="projeto_filtro_ativo.pdf" width="100%" height="500px" title="Projeto de Filtro Ativo"></iframe>
    </div>

    <div class="section">
        <h2>Gráfico de Bode</h2>
        <img src="bode_plot.png" alt="Gráfico de Bode do Filtro" width="100%">
    </div>

    <div class="section">
        <h2>Cálculo para Dual Amplifier Band-Pass</h2>
        <p>
            Código para calcular os valores dos resistores com base no valor do capacitor, com os seguintes parâmetros fixos:<br>
            - Frequência central: <strong>F₀ = 4000 Hz (4 kHz)</strong><br>
            - Ganho: <strong>V₀/Vᵢ = 2 (6 dB)</strong><br>
            - Fator de qualidade: <strong>Q = 10</strong><br>
            Observação: O código já gera um gráfico de Bode. Arquivos com nome "Draw1" são simulações no LTspice que podem ser abertos e simulados no software.
        </p>
    </div>
