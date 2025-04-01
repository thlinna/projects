import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Container, 
  Box, 
  Typography, 
  TextField, 
  Button, 
  Grid, 
  Paper,
  Alert,
  Divider
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login, user, error: authError, resetError } = useAuth();
  const navigate = useNavigate();

  // Jos käyttäjä on jo kirjautunut, ohjaa dashboard-sivulle
  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
    
    // Nollaa virheet kun komponentti tuhoutuu
    return () => {
      resetError();
    };
  }, [user, navigate, resetError]);

  // Kun autentikaatiovirhe muuttuu, päivitä paikallinen virhetila
  useEffect(() => {
    if (authError) {
      setError(authError);
      setLoading(false);
    }
  }, [authError]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validoi lomake
    if (!email || !password) {
      setError('Sähköposti ja salasana vaaditaan');
      return;
    }
    
    try {
      setError('');
      setLoading(true);
      
      // Yritä kirjautua sisään
      const result = await login(email, password);
      
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.message || 'Kirjautuminen epäonnistui');
      }
    } catch (err) {
      setError('Kirjautumisessa tapahtui virhe');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ my: 8 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Box sx={{ mb: 3, textAlign: 'center' }}>
            <Typography variant="h4" component="h1" gutterBottom>
              Kirjaudu sisään
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Kirjaudu sisään hallitaksesi rahoitushakemuksiasi
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} noValidate>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Sähköpostiosoite"
              name="email"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Salasana"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? 'Kirjaudutaan...' : 'Kirjaudu sisään'}
            </Button>
            
            <Grid container justifyContent="space-between">
              <Grid item>
                <Link to="/forgot-password" style={{ textDecoration: 'none' }}>
                  <Typography variant="body2" color="primary">
                    Unohditko salasanasi?
                  </Typography>
                </Link>
              </Grid>
              <Grid item>
                <Link to="/register" style={{ textDecoration: 'none' }}>
                  <Typography variant="body2" color="primary">
                    Ei tiliä? Rekisteröidy
                  </Typography>
                </Link>
              </Grid>
            </Grid>
          </Box>
          
          <Divider sx={{ my: 3 }}>
            <Typography variant="body2" color="textSecondary">
              TAI
            </Typography>
          </Divider>
          
          <Button
            fullWidth
            variant="outlined"
            component={Link}
            to="/"
            sx={{ mt: 1 }}
          >
            Takaisin etusivulle
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default LoginPage; 