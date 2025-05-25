import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';
import {
  Box,
  Paper,
  Typography,
  Button,
  CircularProgress,
  styled,
} from '@mui/material';
import { Location } from '../types';

const DetailsContainer = styled(Paper)(({ theme }) => ({
  position: 'absolute',
  top: theme.spacing(2),
  right: theme.spacing(2),
  width: '400px',
  maxHeight: 'calc(100vh - 80px)',
  overflow: 'auto',
  padding: theme.spacing(2),
  backgroundColor: 'rgba(255, 255, 255, 0.95)',
  zIndex: 1000,
}));

const PreviewContainer = styled(Box)({
  width: '100%',
  height: '300px',
  marginBottom: '16px',
  borderRadius: '8px',
  overflow: 'hidden',
});

interface LocationDetailsProps {
  location: Location | null;
  onClose: () => void;
}

const Model: React.FC<{ url: string }> = ({ url }) => {
  const { scene } = useGLTF(url);
  return <primitive object={scene} />;
};

const LocationDetails: React.FC<LocationDetailsProps> = ({ location, onClose }) => {
  if (!location) return null;

  return (
    <DetailsContainer elevation={3}>
      <Typography variant="h5" gutterBottom>
        {location.name}
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        {location.category}
      </Typography>

      <PreviewContainer>
        <Suspense fallback={<CircularProgress />}>
          <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
            <ambientLight intensity={0.5} />
            <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} />
            <Model url={location.threeDModelUrl} />
            <OrbitControls />
          </Canvas>
        </Suspense>
      </PreviewContainer>

      <Typography variant="body1" paragraph>
        {location.summary}
      </Typography>

      <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          color="primary"
          href={location.wikipediaUrl}
          target="_blank"
          rel="noopener noreferrer"
        >
          Read More on Wikipedia
        </Button>
        <Button variant="outlined" onClick={onClose}>
          Close
        </Button>
      </Box>
    </DetailsContainer>
  );
};

export default LocationDetails; 