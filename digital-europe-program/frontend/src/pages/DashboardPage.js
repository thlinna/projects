import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Container, 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CardActions,
  Button,
  Fab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  TextField,
  MenuItem,
  CircularProgress,
  Alert,
  Divider,
  Chip
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { projectAPI } from '../services/api';

// Toimialavaihtoehdot
const domains = [
  'Tekoäly',
  'Kyberturvallisuus',
  'Digitaaliset taidot',
  'Digitaalinen infrastruktuuri',
  'Julkiset palvelut',
  'Terveydenhuolto',
  'Koulutus',
  'Muu'
];

const DashboardPage = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [newProjectData, setNewProjectData] = useState({
    name: '',
    description: '',
    domain: '',
    tags: ''
  });
  const [submitLoading, setSubmitLoading] = useState(false);
  
  const { user } = useAuth();
  const navigate = useNavigate();
  
  // Hae projektit kun komponentti latautuu
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const response = await projectAPI.getProjects();
        setProjects(response.data.data);
      } catch (err) {
        setError('Projektien hakeminen epäonnistui');
        console.error('Virhe projektien haussa:', err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchProjects();
  }, []);
  
  const handleOpenDialog = () => {
    setOpenDialog(true);
  };
  
  const handleCloseDialog = () => {
    setOpenDialog(false);
    // Tyhjennä lomake
    setNewProjectData({
      name: '',
      description: '',
      domain: '',
      tags: ''
    });
  };
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewProjectData(prev => ({
      ...prev,
      [name]: value
    }));
  };
  
  const handleCreateProject = async (e) => {
    e.preventDefault();
    
    // Validoi lomake
    if (!newProjectData.name || !newProjectData.description || !newProjectData.domain) {
      setError('Nimi, kuvaus ja toimiala ovat pakollisia');
      return;
    }
    
    try {
      setSubmitLoading(true);
      setError('');
      
      // Muunna tagit arrayksi
      const formattedData = {
        ...newProjectData,
        tags: newProjectData.tags ? newProjectData.tags.split(',').map(tag => tag.trim()) : []
      };
      
      // Lähetä uusi projekti
      const response = await projectAPI.createProject(formattedData);
      
      // Lisää uusi projekti listaan
      setProjects(prev => [response.data.data, ...prev]);
      
      // Sulje dialogi
      handleCloseDialog();
      
      // Siirry uuden projektin sivulle
      navigate(`/projects/${response.data.data._id}`);
    } catch (err) {
      setError('Projektin luominen epäonnistui: ' + (err.response?.data?.message || err.message));
    } finally {
      setSubmitLoading(false);
    }
  };
  
  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'planning':
        return 'info';
      case 'completed':
        return 'primary';
      default:
        return 'default';
    }
  };
  
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Grid container justifyContent="space-between" alignItems="center">
          <Grid item>
            <Typography variant="h4" component="h1" gutterBottom>
              Projektit
            </Typography>
          </Grid>
          <Grid item>
            <Fab 
              color="primary" 
              aria-label="Lisää projekti"
              onClick={handleOpenDialog}
            >
              <AddIcon />
            </Fab>
          </Grid>
        </Grid>
        
        {error && (
          <Alert severity="error" sx={{ mt: 2, mb: 2 }}>
            {error}
          </Alert>
        )}
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        ) : projects.length === 0 ? (
          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Typography variant="h6" color="textSecondary" gutterBottom>
              Ei projekteja vielä
            </Typography>
            <Typography variant="body1" color="textSecondary" paragraph>
              Aloita luomalla ensimmäinen projektisi.
            </Typography>
            <Button 
              variant="contained" 
              onClick={handleOpenDialog}
              startIcon={<AddIcon />}
            >
              Luo projekti
            </Button>
          </Box>
        ) : (
          <Grid container spacing={3} sx={{ mt: 2 }}>
            {projects.map((project) => (
              <Grid item xs={12} sm={6} md={4} key={project._id}>
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography variant="h5" component="h2" gutterBottom noWrap>
                      {project.name}
                    </Typography>
                    <Chip 
                      label={project.domain} 
                      size="small" 
                      color="primary" 
                      variant="outlined"
                      sx={{ mb: 2 }}
                    />
                    <Typography variant="body2" color="textSecondary" paragraph>
                      {project.description.length > 120 
                        ? `${project.description.substring(0, 120)}...` 
                        : project.description}
                    </Typography>
                    
                    <Box sx={{ mt: 2 }}>
                      <Grid container spacing={1}>
                        <Grid item>
                          <Chip 
                            label={`${project.ideas?.length || 0} ideaa`} 
                            size="small" 
                            variant="outlined"
                          />
                        </Grid>
                        <Grid item>
                          <Chip 
                            label={`${project.applications?.length || 0} hakemusta`} 
                            size="small" 
                            variant="outlined"
                          />
                        </Grid>
                        <Grid item>
                          <Chip 
                            label={project.status || 'aktiivinen'} 
                            size="small"
                            color={getStatusColor(project.status)}
                            variant="outlined"
                          />
                        </Grid>
                      </Grid>
                    </Box>
                  </CardContent>
                  <Divider />
                  <CardActions>
                    <Button 
                      size="small" 
                      component={Link} 
                      to={`/projects/${project._id}`}
                      fullWidth
                    >
                      Avaa projekti
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
      
      {/* Uusi projekti -dialogi */}
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Luo uusi projekti</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Täytä projektin tiedot aloittaaksesi ideointiprosessin.
          </DialogContentText>
          <TextField
            autoFocus
            margin="normal"
            name="name"
            label="Projektin nimi"
            type="text"
            fullWidth
            variant="outlined"
            value={newProjectData.name}
            onChange={handleInputChange}
            required
          />
          <TextField
            margin="normal"
            name="description"
            label="Kuvaus"
            type="text"
            fullWidth
            variant="outlined"
            multiline
            rows={4}
            value={newProjectData.description}
            onChange={handleInputChange}
            required
          />
          <TextField
            margin="normal"
            name="domain"
            select
            label="Toimiala"
            fullWidth
            variant="outlined"
            value={newProjectData.domain}
            onChange={handleInputChange}
            required
          >
            {domains.map((option) => (
              <MenuItem key={option} value={option}>
                {option}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="normal"
            name="tags"
            label="Avainsanat (pilkulla eroteltuna)"
            type="text"
            fullWidth
            variant="outlined"
            value={newProjectData.tags}
            onChange={handleInputChange}
            helperText="Esim: tekoäly, koneoppiminen, digitalisaatio"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Peruuta</Button>
          <Button 
            onClick={handleCreateProject} 
            variant="contained" 
            color="primary"
            disabled={submitLoading}
          >
            {submitLoading ? 'Luodaan...' : 'Luo projekti'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default DashboardPage; 