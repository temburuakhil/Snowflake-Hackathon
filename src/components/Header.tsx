import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  TextField,
  Box,
  Chip,
  IconButton,
  InputAdornment,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import { LocationCategory } from '../types';

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  color: theme.palette.text.primary,
  boxShadow: theme.shadows[2],
}));

const SearchField = styled(TextField)(({ theme }) => ({
  width: '300px',
  '& .MuiOutlinedInput-root': {
    backgroundColor: theme.palette.background.default,
    borderRadius: theme.shape.borderRadius,
  },
}));

const CategoryChip = styled(Chip)(({ theme }) => ({
  margin: theme.spacing(0.5),
  '&.MuiChip-root': {
    backgroundColor: theme.palette.background.default,
    '&:hover': {
      backgroundColor: theme.palette.action.hover,
    },
  },
  '&.selected': {
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
  },
}));

interface HeaderProps {
  onSearch: (query: string) => void;
  selectedCategories: LocationCategory[];
  onCategoryToggle: (category: LocationCategory) => void;
}

const Header: React.FC<HeaderProps> = ({
  onSearch,
  selectedCategories,
  onCategoryToggle,
}) => {
  const categories: LocationCategory[] = [
    'Wildlife Sanctuary',
    'Forest Reserve',
    'National Park',
    'Botanical Garden',
    'Scenic Place',
    'Temple',
  ];

  return (
    <StyledAppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 0, mr: 3 }}>
          IndiaTrek Vista
        </Typography>

        <SearchField
          placeholder="Search locations..."
          variant="outlined"
          size="small"
          onChange={(e) => onSearch(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />

        <Box sx={{ ml: 3, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {categories.map((category) => (
            <CategoryChip
              key={category}
              label={category}
              onClick={() => onCategoryToggle(category)}
              className={selectedCategories.includes(category) ? 'selected' : ''}
            />
          ))}
        </Box>
      </Toolbar>
    </StyledAppBar>
  );
};

export default Header; 