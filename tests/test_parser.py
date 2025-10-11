"""
Unit tests for LLM Response Parser
"""

import pytest
import json
from src.utils.parser import LLMResponseParser
from src.config import VALID_CHANNELS, MIN_PRIORITY, MAX_PRIORITY, DEFAULT_VALUES

class TestLLMResponseParser:
    """Test cases for LLMResponseParser"""
    
    def test_parse_valid_json_response(self):
        """Test parsing of valid JSON response"""
        valid_response = '{"channel": "Email", "priority": 8, "to_agent": true, "notes": "High priority lead"}'
        result = LLMResponseParser.parse_llm_response(valid_response)
        
        assert result["channel"] == "Email"
        assert result["priority"] == 8
        assert result["to_agent"] is True
        assert result["notes"] == "High priority lead"
    
    def test_parse_json_with_markdown(self):
        """Test parsing JSON wrapped in markdown code blocks"""
        markdown_response = '```json\n{"channel": "Phone", "priority": 9, "to_agent": false, "notes": "Call back"}```'
        result = LLMResponseParser.parse_llm_response(markdown_response)
        
        assert result["channel"] == "Phone"
        assert result["priority"] == 9
        assert result["to_agent"] is False
        assert result["notes"] == "Call back"
    
    def test_parse_json_with_extra_text(self):
        """Test parsing JSON with surrounding text"""
        mixed_response = 'Here is the analysis: {"channel": "WhatsApp", "priority": 7, "to_agent": true, "notes": "Quick response needed"} Please review.'
        result = LLMResponseParser.parse_llm_response(mixed_response)
        
        assert result["channel"] == "WhatsApp"
        assert result["priority"] == 7
        assert result["to_agent"] is True
        assert result["notes"] == "Quick response needed"
    
    def test_parse_malformed_json_falls_back_to_defaults(self):
        """Test that malformed JSON falls back to default values"""
        malformed_response = '{"channel": "InvalidChannel", "priority": "not_a_number", "to_agent": "maybe", "notes": 123}'
        result = LLMResponseParser.parse_llm_response(malformed_response)
        
        assert result["channel"] == DEFAULT_VALUES["channel"]
        assert result["priority"] == DEFAULT_VALUES["priority"]
        assert result["to_agent"] == DEFAULT_VALUES["to_agent"]
        assert result["notes"] == DEFAULT_VALUES["notes"]
    
    def test_parse_invalid_json_falls_back_to_defaults(self):
        """Test that invalid JSON falls back to default values"""
        invalid_response = 'This is not JSON at all'
        result = LLMResponseParser.parse_llm_response(invalid_response)
        
        assert result == DEFAULT_VALUES.copy()
    
    def test_parse_empty_response_falls_back_to_defaults(self):
        """Test that empty response falls back to default values"""
        empty_response = ''
        result = LLMResponseParser.parse_llm_response(empty_response)
        
        assert result == DEFAULT_VALUES.copy()
    
    def test_validate_channel_field(self):
        """Test channel field validation"""
        # Valid channels
        for channel in VALID_CHANNELS:
            response = {"channel": channel, "priority": 5, "to_agent": False, "notes": "Test"}
            validated = LLMResponseParser._validate_response(response)
            assert validated["channel"] == channel
        
        # Invalid channel
        response = {"channel": "InvalidChannel", "priority": 5, "to_agent": False, "notes": "Test"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["channel"] == DEFAULT_VALUES["channel"]
    
    def test_validate_priority_field(self):
        """Test priority field validation"""
        # Valid priorities
        for priority in range(MIN_PRIORITY, MAX_PRIORITY + 1):
            response = {"channel": "Email", "priority": priority, "to_agent": False, "notes": "Test"}
            validated = LLMResponseParser._validate_response(response)
            assert validated["priority"] == priority
        
        # Out of range priorities
        response = {"channel": "Email", "priority": 15, "to_agent": False, "notes": "Test"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["priority"] == DEFAULT_VALUES["priority"]
        
        response = {"channel": "Email", "priority": -1, "to_agent": False, "notes": "Test"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["priority"] == DEFAULT_VALUES["priority"]
        
        # Invalid priority types
        response = {"channel": "Email", "priority": "high", "to_agent": False, "notes": "Test"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["priority"] == DEFAULT_VALUES["priority"]
    
    def test_validate_to_agent_field(self):
        """Test to_agent field validation"""
        # Valid boolean values
        response = {"channel": "Email", "priority": 5, "to_agent": True, "notes": "Test"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["to_agent"] is True
        
        response = {"channel": "Email", "priority": 5, "to_agent": False, "notes": "Test"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["to_agent"] is False
        
        # String representations
        response = {"channel": "Email", "priority": 5, "to_agent": "true", "notes": "Test"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["to_agent"] is True
        
        response = {"channel": "Email", "priority": 5, "to_agent": "false", "notes": "Test"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["to_agent"] is False
        
        # Invalid values
        response = {"channel": "Email", "priority": 5, "to_agent": "maybe", "notes": "Test"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["to_agent"] == DEFAULT_VALUES["to_agent"]
    
    def test_validate_notes_field(self):
        """Test notes field validation"""
        # Valid notes
        response = {"channel": "Email", "priority": 5, "to_agent": False, "notes": "Valid notes"}
        validated = LLMResponseParser._validate_response(response)
        assert validated["notes"] == "Valid notes"
        
        # Long notes get truncated
        long_notes = "A" * 250
        response = {"channel": "Email", "priority": 5, "to_agent": False, "notes": long_notes}
        validated = LLMResponseParser._validate_response(response)
        assert len(validated["notes"]) <= 200
        assert validated["notes"].endswith("...")
        
        # Empty notes
        response = {"channel": "Email", "priority": 5, "to_agent": False, "notes": ""}
        validated = LLMResponseParser._validate_response(response)
        assert validated["notes"] == DEFAULT_VALUES["notes"]
    
    def test_is_valid_response(self):
        """Test response validation method"""
        # Valid response
        valid_response = {
            "channel": "Email",
            "priority": 8,
            "to_agent": True,
            "notes": "High priority lead"
        }
        assert LLMResponseParser.is_valid_response(valid_response) is True
        
        # Invalid responses
        invalid_responses = [
            {"channel": "InvalidChannel", "priority": 8, "to_agent": True, "notes": "Test"},
            {"channel": "Email", "priority": 15, "to_agent": True, "notes": "Test"},
            {"channel": "Email", "priority": 8, "to_agent": "maybe", "notes": "Test"},
            {"channel": "Email", "priority": 8, "to_agent": True, "notes": 123},
            {"channel": "Email", "priority": 8, "to_agent": True},  # Missing notes
        ]
        
        for response in invalid_responses:
            assert LLMResponseParser.is_valid_response(response) is False
    
    def test_clean_response_string(self):
        """Test response string cleaning"""
        # Test markdown removal
        response = '```json\n{"test": "value"}```'
        cleaned = LLMResponseParser._clean_response_string(response)
        assert cleaned == '{"test": "value"}'
        
        # Test extra text removal
        response = 'Before {"test": "value"} After'
        cleaned = LLMResponseParser._clean_response_string(response)
        assert cleaned == '{"test": "value"}'
        
        # Test whitespace removal
        response = '  {"test": "value"}  '
        cleaned = LLMResponseParser._clean_response_string(response)
        assert cleaned == '{"test": "value"}'
    
    def test_edge_cases(self):
        """Test various edge cases"""
        # None response
        result = LLMResponseParser.parse_llm_response(None)
        assert result == DEFAULT_VALUES.copy()
        
        # Response with only partial fields
        partial_response = '{"channel": "Email"}'
        result = LLMResponseParser.parse_llm_response(partial_response)
        assert result["channel"] == "Email"
        assert result["priority"] == DEFAULT_VALUES["priority"]
        assert result["to_agent"] == DEFAULT_VALUES["to_agent"]
        assert result["notes"] == DEFAULT_VALUES["notes"]
        
        # Response with extra fields
        extra_fields_response = '{"channel": "Phone", "priority": 6, "to_agent": false, "notes": "Test", "extra": "field"}'
        result = LLMResponseParser.parse_llm_response(extra_fields_response)
        assert result["channel"] == "Phone"
        assert result["priority"] == 6
        assert result["to_agent"] is False
        assert result["notes"] == "Test"
        assert "extra" not in result

if __name__ == "__main__":
    pytest.main([__file__])



