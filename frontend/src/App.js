import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Rules from './pages/Rules';
import Logs from './pages/Logs';
import Settings from './pages/Settings';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route path="/" exact component={Dashboard} />
        <Route path="/rules" component={Rules} />
        <Route path="/logs" component={Logs} />
        <Route path="/settings" component={Settings} />
      </Switch>
    </Router>
  );
}

export default App;