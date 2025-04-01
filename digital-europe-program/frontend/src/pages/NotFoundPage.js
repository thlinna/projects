import React from 'react';
import { Link } from 'react-router-dom';
import { Box, Container, Typography, Button, Paper } from '@mui/material';

const NotFoundPage = () => {
  return (
    <Container maxWidth="sm">
      <Box sx={{ 
        mt: 8, 
        mb: 8, 
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        textAlign: 'center' 
      }}>
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography variant="h1" component="h1" gutterBottom sx={{ fontSize: '4rem' }}>
            404
          </Typography>
          <Typography variant="h4" component="h2" gutterBottom>
            Sivua ei löydy
          </Typography>
          <Typography variant="body1" paragraph color="textSecondary">
            Valitettavasti hakemaasi sivua ei löytynyt. Se on saattanut poistua tai osoite on virheellinen.
          </Typography>
          <Box sx={{ mt: 4 }}>
            <Button 
              component={Link} 
              to="/" 
              variant="contained" 
              color="primary" 
              size="large"
              sx={{ mb: 2 }}
            >
              Palaa etusivulle
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default NotFoundPage; 