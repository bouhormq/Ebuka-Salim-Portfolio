#!/bin/bash

# Timeline Post API Testing Script
# This script tests the POST, GET, and DELETE endpoints for timeline posts

# Configuration
BASE_URL="http://localhost:5001"
API_URL="$BASE_URL/api/timeline_post"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Generate random test data
generate_random_data() {
    NAMES=("Alice Johnson" "Bob Smith" "Charlie Brown" "Diana Prince" "Eve Wilson")
    DOMAINS=("gmail.com" "yahoo.com" "hotmail.com" "example.com")
    CONTENT_SAMPLES=(
        "Just finished an amazing project!"
        "Learning new technologies every day."
        "Excited about the future of web development."
        "Working on some cool features today."
        "Coffee and code make the perfect combination."
    )
    
    # Select random values
    RANDOM_NAME=${NAMES[$RANDOM % ${#NAMES[@]}]}
    RANDOM_DOMAIN=${DOMAINS[$RANDOM % ${#DOMAINS[@]}]}
    RANDOM_EMAIL="${RANDOM_NAME// /}$(($RANDOM % 1000))@$RANDOM_DOMAIN"
    RANDOM_CONTENT=${CONTENT_SAMPLES[$RANDOM % ${#CONTENT_SAMPLES[@]}]}
}

# Test if server is running
test_server() {
    print_status "Testing if server is running..."
    if curl -s --connect-timeout 5 "$BASE_URL" > /dev/null; then
        print_success "Server is running at $BASE_URL"
        return 0
    else
        print_error "Server is not running at $BASE_URL"
        print_warning "Please start your Flask application first"
        exit 1
    fi
}

# Test GET endpoint (initial state)
test_get_initial() {
    print_status "Testing GET endpoint (initial state)..."
    INITIAL_RESPONSE=$(curl -s -X GET "$API_URL")
    
    if [ $? -eq 0 ]; then
        print_success "GET request successful"
        echo "Response: $INITIAL_RESPONSE"
        
        # Count initial posts
        INITIAL_COUNT=$(echo "$INITIAL_RESPONSE" | grep -o '"timeline_posts":\[' | wc -l)
        echo "Initial timeline posts found: $INITIAL_COUNT"
    else
        print_error "GET request failed"
        exit 1
    fi
}

# Test POST endpoint
test_post() {
    print_status "Testing POST endpoint..."
    generate_random_data
    
    print_status "Creating timeline post with:"
    echo "  Name: $RANDOM_NAME"
    echo "  Email: $RANDOM_EMAIL"
    echo "  Content: $RANDOM_CONTENT"
    
    POST_RESPONSE=$(curl -s -X POST "$API_URL" \
        -d "name=$RANDOM_NAME" \
        -d "email=$RANDOM_EMAIL" \
        -d "content=$RANDOM_CONTENT")
    
    if [ $? -eq 0 ]; then
        print_success "POST request successful"
        echo "Response: $POST_RESPONSE"
        
        # Extract the ID from the response (handle the compact JSON format)
        POST_ID=$(echo "$POST_RESPONSE" | sed 's/.*"id":\([0-9]*\).*/\1/')
        if [ -n "$POST_ID" ] && [ "$POST_ID" != "$POST_RESPONSE" ]; then
            print_success "Created timeline post with ID: $POST_ID"
            return 0
        else
            print_warning "Could not extract ID from response"
            return 1
        fi
    else
        print_error "POST request failed"
        exit 1
    fi
}

# Test GET endpoint (after POST)
test_get_after_post() {
    print_status "Testing GET endpoint (after POST)..."
    UPDATED_RESPONSE=$(curl -s -X GET "$API_URL")
    
    if [ $? -eq 0 ]; then
        print_success "GET request successful"
        echo "Response: $UPDATED_RESPONSE"
        
        # Verify the post was added
        if echo "$UPDATED_RESPONSE" | grep -q "$RANDOM_NAME"; then
            print_success "New timeline post found in GET response!"
        else
            print_error "New timeline post NOT found in GET response"
            return 1
        fi
    else
        print_error "GET request failed"
        exit 1
    fi
}

# Test DELETE endpoint
test_delete() {
    if [ -n "$POST_ID" ]; then
        print_status "Testing DELETE endpoint for post ID: $POST_ID..."
        DELETE_RESPONSE=$(curl -s -X DELETE "$API_URL/$POST_ID")
        
        if [ $? -eq 0 ]; then
            print_success "DELETE request successful"
            echo "Response: $DELETE_RESPONSE"
            
            # Verify deletion
            print_status "Verifying deletion..."
            VERIFY_RESPONSE=$(curl -s -X GET "$API_URL")
            if echo "$VERIFY_RESPONSE" | grep -q "\"id\":$POST_ID"; then
                print_error "Post still exists after deletion"
                return 1
            else
                print_success "Post successfully deleted"
                return 0
            fi
        else
            print_error "DELETE request failed"
            return 1
        fi
    else
        print_warning "No POST_ID available for deletion test"
        return 1
    fi
}

# Main execution
main() {
    echo "========================================="
    echo "Timeline Post API Testing Script"
    echo "========================================="
    
    # Run tests
    test_server
    test_get_initial
    test_post
    test_get_after_post
    test_delete
    
    echo "========================================="
    print_success "All tests completed!"
    echo "========================================="
}

# Run the main function
main
