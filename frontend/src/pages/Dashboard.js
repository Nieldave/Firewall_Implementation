import React from 'react';
import { Container, Typography } from '@material-ui/core';

const Dashboard = () => {
  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Typography variant="body1">
        Welcome to the Firewall Dashboard. Here you can monitor and manage your firewall settings.
      </Typography>
      {/* Add more dashboard components and statistics here */}
    </Container>
  );
};

export default Dashboard;