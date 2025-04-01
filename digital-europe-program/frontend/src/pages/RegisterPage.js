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
  Divider,
  InputAdornment,
  IconButton
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const RegisterPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { register, user, error: authError, resetError } = useAuth();
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

  const handleTogglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validoi lomake
    if (!name || !email || !password || !passwordConfirm) {
      setError('Kaikki kentät ovat pakollisia');
      return;
    }
    
    if (password !== passwordConfirm) {
      setError('Salasanat eivät täsmää');
      return;
    }
    
    if (password.length < 6) {
      setError('Salasanan tulee olla vähintään 6 merkkiä pitkä');
      return;
    }
    
    try {
      setError('');
      setLoading(true);
      
      // Yritä rekisteröityä
      const result = await register({
        name,
        email,
        password
      });
      
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.message || 'Rekisteröityminen epäonnistui');
      }
    } catch (err) {
      setError('Rekisteröitymisessä tapahtui virhe');
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
              Luo uusi tili
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Rekisteröidy käyttääksesi Digital Europe Program -työkalua
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
              id="name"
              label="Nimi"
              name="name"
              autoComplete="name"
              autoFocus
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={loading}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Sähköpostiosoite"
              name="email"
              autoComplete="email"
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
              type={showPassword ? 'text' : 'password'}
              id="password"
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={loading}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleTogglePasswordVisibility}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="passwordConfirm"
              label="Vahvista salasana"
              type={showPassword ? 'text' : 'password'}
              id="passwordConfirm"
              value={passwordConfirm}
              onChange={(e) => setPasswordConfirm(e.target.value)}
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
              {loading ? 'Rekisteröidytään...' : 'Rekisteröidy'}
            </Button>
            
            <Grid container justifyContent="center">
              <Grid item>
                <Link to="/login" style={{ textDecoration: 'none' }}>
                  <Typography variant="body2" color="primary">
                    Onko sinulla jo tili? Kirjaudu sisään
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

export default RegisterPage; 