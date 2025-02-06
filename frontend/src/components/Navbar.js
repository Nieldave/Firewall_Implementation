import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button } from '@material-ui/core';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" style={{ flexGrow: 1 }}>
          Firewall Dashboard
        </Typography>
        <Button color="inherit" component={Link} to="/">Dashboard</Button>
        <Button color="inherit" component={Link} to="/rules">Rules</Button>
        <Button color="inherit" component={Link} to="/logs">Logs</Button>
        <Button color="inherit" component={Link} to="/settings">Settings</Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;