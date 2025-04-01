import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Box, 
  Container, 
  Typography, 
  Button, 
  Grid, 
  Card, 
  CardContent, 
  CardActions,
  CardMedia
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const HomePage = () => {
  const { user } = useAuth();

  return (
    <Box>
      {/* Hero-osio */}
      <Box 
        sx={{ 
          bgcolor: 'primary.main', 
          color: 'white', 
          py: 8 
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h1" component="h1" gutterBottom>
                Digital Europe Program
              </Typography>
              <Typography variant="h5" paragraph>
                Tekoälyavusteinen työkalu rahoitushakemusten ideointiin ja valmisteluun
              </Typography>
              {user ? (
                <Button 
                  component={Link} 
                  to="/dashboard" 
                  variant="contained" 
                  color="secondary" 
                  size="large"
                >
                  Siirry hallintapaneeliin
                </Button>
              ) : (
                <Box>
                  <Button 
                    component={Link} 
                    to="/register" 
                    variant="contained" 
                    color="secondary" 
                    size="large" 
                    sx={{ mr: 2 }}
                  >
                    Rekisteröidy
                  </Button>
                  <Button 
                    component={Link} 
                    to="/login" 
                    variant="outlined" 
                    color="inherit" 
                    size="large"
                  >
                    Kirjaudu sisään
                  </Button>
                </Box>
              )}
            </Grid>
            <Grid item xs={12} md={6}>
              <Box sx={{ textAlign: 'center' }}>
                <img 
                  src="/images/hero-image.png" 
                  alt="Digital Europe Program" 
                  style={{ 
                    maxWidth: '100%', 
                    height: 'auto',
                    display: 'inline-block'
                  }} 
                />
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Ominaisuudet */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography variant="h2" component="h2" align="center" gutterBottom>
          Miten järjestelmä toimii
        </Typography>
        <Typography variant="body1" align="center" paragraph sx={{ mb: 6 }}>
          Neljä tekoälyagenttia auttaa sinua rahoitushakemuksen jokaisessa vaiheessa
        </Typography>

        <Grid container spacing={4}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardMedia
                component="img"
                height="140"
                image="/images/ideanikkari.png"
                alt="Ideanikkari"
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h5" component="h3">
                  Ideanikkari
                </Typography>
                <Typography>
                  Auttaa sinua kehittämään innovatiivisia ideoita rahoitushakemuksia varten. Ehdottaa luovia ja toteutettavissa olevia projekteja.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardMedia
                component="img"
                height="140"
                image="/images/arvioija.png"
                alt="Arvioija"
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h5" component="h3">
                  Arvioija
                </Typography>
                <Typography>
                  Arvioi ideoitasi kriittisesti ja antaa rakentavaa palautetta. Auttaa vahvistamaan hakemustasi ennen lähetystä.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardMedia
                component="img"
                height="140"
                image="/images/hakija.png"
                alt="Hakija"
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h5" component="h3">
                  Hakija
                </Typography>
                <Typography>
                  Muuntaa ideasi viralliseksi hakemukseksi. Varmistaa, että kaikki vaaditut osiot ovat mukana ja muotoiltu oikein.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardMedia
                component="img"
                height="140"
                image="/images/rahoittaja.png"
                alt="Rahoittaja"
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography gutterBottom variant="h5" component="h3">
                  Rahoittaja
                </Typography>
                <Typography>
                  Arvioi hakemuksesi rahoittajan näkökulmasta. Antaa yksityiskohtaista palautetta ja parannusehdotuksia.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>

      {/* Call to Action */}
      <Box sx={{ bgcolor: 'secondary.main', color: 'white', py: 6 }}>
        <Container maxWidth="lg">
          <Typography variant="h3" component="h3" align="center" gutterBottom>
            Aloita rahoitushakemuksesi valmistelu tänään
          </Typography>
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            {user ? (
              <Button 
                component={Link} 
                to="/dashboard" 
                variant="contained" 
                color="primary" 
                size="large"
              >
                Siirry hallintapaneeliin
              </Button>
            ) : (
              <Button 
                component={Link} 
                to="/register" 
                variant="contained" 
                color="primary" 
                size="large"
              >
                Luo ilmainen tunnus
              </Button>
            )}
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage; 