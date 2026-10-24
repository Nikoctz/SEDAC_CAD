import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import GlobalStyle from './GlobalStyle';
import './styles.css';
import './app.css';

globalThis.React = React;

globalThis.ReactDOM = ReactDOM;

const root = document.getElementById('root');
if (!root) throw new Error('Root not found');

ReactDOM.createRoot(root).render(
  React.createElement(
    React.StrictMode,
    null,
    React.createElement(GlobalStyle, null),
    React.createElement(App, null)
  )
);
